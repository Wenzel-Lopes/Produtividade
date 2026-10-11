"""Gera fontes originais e determinísticas. Nenhuma entrada empresarial é lida."""
import calendar
import json
import random
from datetime import date, timedelta
from pathlib import Path

SEED = 42
DEPARTMENTS = [(1, "Operações"), (2, "Tecnologia"), (3, "Comercial"), (4, "Administrativo")]


def generate(directory, seed=SEED):
    rng = random.Random(seed)
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    employees = []
    for i in range(1, 241):
        hire = date(2023, 1, 1) + timedelta(days=rng.randrange(700))
        if i > 210:
            hire = date(2025, 1, 1) + timedelta(days=(i - 211) * 6)
        end = None
        if i <= 36:
            end = date(2025, 1, 1) + timedelta(days=(i - 1) * 5)
        employees.append(dict(employee_id=i, department_id=1+(i%4),
                              hired_on=hire.isoformat(), ended_on=end.isoformat() if end else None,
                              salary_cents=rng.randrange(2500, 11001, 100)*100,
                              updated_at="2025-07-01T00:00:00Z"))
    facts = []
    for m in range(1, 7):
        first = date(2025, m, 1)
        last = date(2025, m, calendar.monthrange(2025, m)[1])
        for e in employees:
            hire = date.fromisoformat(e["hired_on"])
            end = date.fromisoformat(e["ended_on"]) if e["ended_on"] else last + timedelta(days=1)
            # ended_on é o primeiro dia inativo (intervalo [admissão, desligamento)).
            start, stop = max(first, hire), min(last+timedelta(days=1), end)
            if stop <= start:
                continue
            days = (stop-start).days
            weekdays = sum((start+timedelta(days=k)).weekday()<5 for k in range(days))
            scheduled = weekdays * 480
            # Parâmetros pedagógicos originais. Cobertura melhora no semestre.
            mapped = int(rng.random() < 0.68 + 0.04*m)
            captured = int(scheduled*rng.uniform(.76,.98)) if mapped else 0
            productive = int(captured*rng.uniform(.56,.82))
            facts.append(dict(employee_id=e["employee_id"], month=first.isoformat(),
                              payroll_cents=round(e["salary_cents"]*days/last.day),
                              scheduled_minutes=scheduled, captured_minutes=captured,
                              productive_minutes=productive, mapped=mapped,
                              updated_at="2025-07-01T00:00:00Z"))
    departments = [dict(department_id=i,name=n,updated_at="2025-07-01T00:00:00Z") for i,n in DEPARTMENTS]
    base = dict(schema_version=1, synthetic=True, seed=seed, departments=departments,
                employees=employees, facts=[r for r in facts if r["month"] < "2025-06-01"])
    delta = dict(schema_version=1, synthetic=True, seed=seed, departments=[],employees=[],
                 facts=[r for r in facts if r["month"] == "2025-06-01"])
    correction = next(r.copy() for r in facts if r["month"] == "2025-03-01" and r["employee_id"]==100)
    correction["payroll_cents"] += 15000
    correction["updated_at"] = "2025-07-02T00:00:00Z"
    delta["facts"].append(correction)
    for name, batch in [("001_base.json", base), ("002_incremental.json",delta)]:
        (directory/name).write_text(json.dumps(batch,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return {"employees":len(employees),"monthly_rows":len(facts),"seed":seed}
