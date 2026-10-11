import copy
import json
import os
import tempfile
import unittest
from pathlib import Path
from produtividade.generate import generate
from produtividade.db import Database, ROOT
from produtividade.etl import load_batch
from produtividade.analyze import summarize


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.path=Path(self.temp.name)
        generate(self.path)
        self.db=Database(":memory:")

    def tearDown(self):
        self.db.close()
        self.temp.cleanup()

    def batch(self,name,body):
        p=self.path/name
        p.write_text(json.dumps(body),encoding="utf-8")
        return p

    def load_base(self):
        return load_batch(self.db,self.path/"001_base.json")

    def test_deterministic_generator(self):
        first=(self.path/"001_base.json").read_bytes()
        generate(self.path)
        self.assertEqual(first,(self.path/"001_base.json").read_bytes())

    def test_replay_is_idempotent(self):
        self.load_base()
        before=self.db.rows("SELECT * FROM monthly_facts ORDER BY employee_id,month")
        r=self.load_base()
        self.assertEqual(r["changed_rows"],0)
        self.assertEqual(before,self.db.rows("SELECT * FROM monthly_facts ORDER BY employee_id,month"))

    def test_late_correction_and_stale_replay(self):
        self.load_base()
        old=self.db.rows("SELECT * FROM monthly_facts WHERE employee_id=100 AND month='2025-03-01'")[0]
        load_batch(self.db,self.path/"002_incremental.json")
        new=self.db.rows("SELECT * FROM monthly_facts WHERE employee_id=100 AND month='2025-03-01'")[0]
        self.assertEqual(new["payroll_cents"],old["payroll_cents"]+15000)
        delta=json.loads((self.path/"002_incremental.json").read_text())
        delta["facts"]=[old]
        self.assertEqual(load_batch(self.db,self.batch("003_stale.json",delta))["changed_rows"],0)

    def test_changed_file_rejected(self):
        self.load_base()
        p=self.path/"001_base.json"
        p.write_text(p.read_text()+" ")
        with self.assertRaisesRegex(ValueError,"alterado"):
            load_batch(self.db,p)

    def test_equal_version_conflict_rolls_back(self):
        self.load_base()
        delta=json.loads((self.path/"002_incremental.json").read_text())
        delta["facts"][-1]["updated_at"]="2025-07-01T00:00:00Z"
        before=self.db.rows("SELECT COUNT(*) AS n FROM monthly_facts")[0]["n"]
        with self.assertRaisesRegex(ValueError,"Mesma chave"):
            load_batch(self.db,self.batch("003_conflict.json",delta))
        self.assertEqual(before,self.db.rows("SELECT COUNT(*) AS n FROM monthly_facts")[0]["n"])
        self.assertEqual(len(self.db.rows("SELECT * FROM etl_batches")),1)

    def test_invalid_reference_rolls_back(self):
        self.load_base()
        delta=json.loads((self.path/"002_incremental.json").read_text())
        delta["facts"][-1]["employee_id"]=99999
        with self.assertRaises(Exception):
            load_batch(self.db,self.batch("003_orphan.json",delta))
        self.assertEqual(self.db.rows("SELECT COUNT(*) AS n FROM monthly_facts WHERE month='2025-06-01'")[0]["n"],0)

    def test_duplicate_key_rejected(self):
        data=json.loads((self.path/"001_base.json").read_text())
        data["facts"].append(copy.deepcopy(data["facts"][0]))
        with self.assertRaisesRegex(ValueError,"duplicada"):
            load_batch(self.db,self.batch("duplicate.json",data))

    def test_metric_reconciliation(self):
        self.load_base()
        load_batch(self.db,self.path/"002_incremental.json")
        result=summarize(self.db)
        for r in result["monthly"]:
            self.assertEqual(r["headcount"],r["opening_headcount"]+r["hires"]-r["exits"])
            for k in ("collection_coverage","mapping_coverage","observed_activity_ratio"):
                self.assertTrue(r[k] is None or 0<=r[k]<=1)
        # Soma independente direto do SQL, não reutiliza o helper de agregação.
        for r in [x for x in result["monthly"] if x["department_id"]==0]:
            total=self.db.rows("SELECT SUM(payroll_cents) AS cents FROM monthly_facts WHERE month=?",(r["month"],))[0]["cents"]
            self.assertAlmostEqual(total/100,r["payroll_brl"])
            parts=[x for x in result["monthly"] if x["month"]==r["month"] and x["department_id"]!=0]
            self.assertEqual(r["headcount"],sum(x["headcount"] for x in parts))
            self.assertAlmostEqual(r["payroll_brl"],sum(x["payroll_brl"] for x in parts))


@unittest.skipUnless(os.environ.get("PRODUTIVIDADE_TEST_POSTGRES")=="1","PostgreSQL de teste não configurado")
class PostgresIntegration(unittest.TestCase):
    def test_load_and_view_match_python(self):
        # Use exclusivamente uma base de teste vazia ou já contendo esta mesma demo.
        db=Database(postgres=True)
        try:
            with tempfile.TemporaryDirectory() as directory:
                generate(directory)
                for f in sorted(Path(directory).glob("*.json")):
                    load_batch(db,f)
                for f in sorted(Path(directory).glob("*.json")):
                    self.assertEqual(load_batch(db,f)["changed_rows"],0)
            db.execute((ROOT/"sql/002_kpis_postgresql.sql").read_text(encoding="utf-8"))
            db.conn.commit()
            sql_rows=db.rows("SELECT * FROM vw_kpis_monthly")
            python_rows={(r["month"],r["department_id"]):r for r in summarize(db)["monthly"] if r["department_id"]}
            self.assertEqual(len(sql_rows),len(python_rows))
            for row in sql_rows:
                ref=python_rows[(str(row["month"]),row["department_id"])]
                for key in ["headcount","opening_headcount","hires","exits","payroll_brl","turnover","mapping_coverage","collection_coverage","observed_activity_ratio"]:
                    self.assertAlmostEqual(float(row[key]),ref[key],places=6)
        finally:
            db.close()


if __name__=="__main__":
    unittest.main()
