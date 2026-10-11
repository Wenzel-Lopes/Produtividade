"""Agregados públicos. Nenhum cadastro individual é exportado para o site."""
import calendar
import csv
import json
from datetime import date, timedelta
from pathlib import Path


def ratio(a,b):
    return a/b if b else None


def summarize(db):
    employees=db.rows("SELECT * FROM employees")
    facts=db.rows("SELECT * FROM monthly_facts ORDER BY month,employee_id")
    departments=db.rows("SELECT * FROM departments ORDER BY department_id")
    monthly=[]
    for month in sorted({r["month"] for r in facts}):
        first=date.fromisoformat(month)
        last=date(first.year,first.month,calendar.monthrange(first.year,first.month)[1])
        before=(first-timedelta(days=1)).isoformat()
        for dep in [{"department_id":0,"name":"Todas as áreas"}]+departments:
            es=[e for e in employees if dep["department_id"]==0 or e["department_id"]==dep["department_id"]]
            ids={e["employee_id"] for e in es}
            fs=[f for f in facts if f["month"]==month and f["employee_id"] in ids]
            def active(on):
                return sum(e["hired_on"]<=on and (e["ended_on"] is None or e["ended_on"]>on) for e in es)
            opening, closing=active(before),active(last.isoformat())
            exits=sum(bool(e["ended_on"] and month<=e["ended_on"]<=last.isoformat()) for e in es)
            hires=sum(month<=e["hired_on"]<=last.isoformat() for e in es)
            scheduled=sum(f["scheduled_minutes"] for f in fs)
            captured=sum(f["captured_minutes"] for f in fs)
            productive=sum(f["productive_minutes"] for f in fs)
            monthly.append(dict(month=month,department_id=dep["department_id"],department=dep["name"],
                opening_headcount=opening,headcount=closing,hires=hires,exits=exits,
                payroll_brl=sum(f["payroll_cents"] for f in fs)/100,
                turnover=ratio(exits,(opening+closing)/2),
                mapping_coverage=ratio(sum(f["mapped"] for f in fs),len(fs)),
                collection_coverage=ratio(captured,scheduled),
                observed_activity_ratio=ratio(productive,captured),
                eligible_employees=len(fs),mapped_employees=sum(f["mapped"] for f in fs),
                scheduled_minutes=scheduled,captured_minutes=captured,productive_minutes=productive))
    return {"synthetic":True,"period":"Janeiro a junho de 2025", "seed":42,
            "definitions_version":"1.0", "monthly":monthly,
            "limitations":["Dados inteiramente fictícios.","Atividade digital é uma proxy simulada, não uma medida de valor ou desempenho individual.",
                            "Folha é salário-base proporcional com uma correção demonstrativa; exclui encargos e benefícios."]}


def export(db, destination="site", report_dir="reports"):
    data=summarize(db)
    destination,report_dir=Path(destination),Path(report_dir)
    destination.mkdir(parents=True,exist_ok=True)
    report_dir.mkdir(parents=True,exist_ok=True)
    text=json.dumps(data,ensure_ascii=False,indent=2)
    (report_dir/"metrics.json").write_text(text+"\n",encoding="utf-8")
    (destination/"data.js").write_text("window.PRODUTIVIDADE_DATA = "+text+";\n",encoding="utf-8")
    with (report_dir/"metrics.csv").open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(data["monthly"][0]) if data["monthly"] else ["month"])
        writer.writeheader()
        writer.writerows(data["monthly"])
    return data
