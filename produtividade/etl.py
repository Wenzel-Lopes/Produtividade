"""Carga atômica por lote, idempotente e com proteção contra versões antigas."""
import hashlib
import json
from datetime import date, datetime, timezone
from pathlib import Path

SPECS = {
 "departments":("departments",["department_id"],["department_id","name","updated_at"]),
 "employees":("employees",["employee_id"],["employee_id","department_id","hired_on","ended_on","salary_cents","updated_at"]),
 "facts":("monthly_facts",["employee_id","month"],["employee_id","month","payroll_cents","scheduled_minutes","captured_minutes","productive_minutes","mapped","updated_at"])
}


def validate(batch):
    if batch.get("schema_version")!=1 or batch.get("synthetic") is not True:
        raise ValueError("Somente o contrato sintético v1 é aceito")
    for entity,(_,keys,columns) in SPECS.items():
        seen=set()
        for row in batch[entity]:
            if set(row)!=set(columns):
                raise ValueError(f"Colunas inesperadas em {entity}")
            key=tuple(row[k] for k in keys)
            if key in seen:
                raise ValueError(f"Chave duplicada em {entity}: {key}")
            seen.add(key)
            ts=row["updated_at"]
            if datetime.strptime(ts,"%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%dT%H:%M:%SZ")!=ts:
                raise ValueError("Timestamp deve ser UTC no formato canônico")
            for col in columns:
                if col.endswith(("_id","_cents","_minutes")) or col=="mapped":
                    if type(row[col]) is not int or row[col]<0:
                        raise ValueError(f"Inteiro não negativo esperado: {col}")
            for col in ("hired_on","ended_on","month"):
                if row.get(col) is not None:
                    if date.fromisoformat(row[col]).isoformat()!=row[col]:
                        raise ValueError("Data fora do formato ISO")
            if entity=="facts" and not row["month"].endswith("-01"):
                raise ValueError("Mês deve começar no dia 01")


def load_batch(db, filename):
    filename=Path(filename)
    raw=filename.read_bytes()
    digest=hashlib.sha256(raw).hexdigest()
    try:
        # Serializa cargas concorrentes no PostgreSQL. SQLite usa lock de escrita.
        if db.postgres:
            db.execute("SELECT pg_advisory_xact_lock(4242001)")
        else:
            db.execute("BEGIN IMMEDIATE")
        existing=db.rows("SELECT sha256 FROM etl_batches WHERE batch_name=?",(filename.name,))
        if existing:
            if existing[0]["sha256"]!=digest:
                raise ValueError("Lote já processado foi alterado. Gere um novo lote/versionamento.")
            db.conn.commit()
            return {"batch":filename.name,"changed_rows":0,"status":"already_loaded"}
        batch=json.loads(raw)
        validate(batch)
        changed=0
        for entity,(table,keys,columns) in SPECS.items():
            for row in batch[entity]:
                where=" AND ".join(k+"=?" for k in keys)
                old=db.rows(f"SELECT * FROM {table} WHERE {where}",tuple(row[k] for k in keys))
                if old and row["updated_at"]==old[0]["updated_at"] and row!=old[0]:
                    raise ValueError("Mesma chave e versão com conteúdos diferentes")
                if old and row["updated_at"]<=old[0]["updated_at"]:
                    continue
                updates=",".join(f"{c}=excluded.{c}" for c in columns if c not in keys)
                query=f"INSERT INTO {table} ({','.join(columns)}) VALUES ({','.join('?' for _ in columns)}) ON CONFLICT ({','.join(keys)}) DO UPDATE SET {updates} WHERE excluded.updated_at > {table}.updated_at"
                db.execute(query,tuple(row[c] for c in columns))
                changed+=1
        # Rejeita fatos fora do vínculo inclusive quando a correção está no cadastro.
        invalid=db.rows("SELECT f.employee_id,f.month FROM monthly_facts f JOIN employees e ON e.employee_id=f.employee_id")
        employees={r["employee_id"]:r for r in db.rows("SELECT * FROM employees")}
        for r in invalid:
            m=date.fromisoformat(r["month"])
            next_m=date(m.year+(m.month==12),m.month%12+1,1).isoformat()
            e=employees[r["employee_id"]]
            if e["hired_on"]>=next_m or (e["ended_on"] is not None and e["ended_on"]<=r["month"]):
                raise ValueError("Fato mensal fora do intervalo de vínculo")
        db.execute("INSERT INTO etl_batches VALUES (?,?,?,?)",
                   (filename.name,digest,datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),changed))
        db.conn.commit()
        return {"batch":filename.name,"changed_rows":changed,"status":"loaded"}
    except Exception:
        db.conn.rollback()
        raise
