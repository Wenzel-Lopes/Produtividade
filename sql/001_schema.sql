-- Tipos portáveis entre SQLite (demonstração) e PostgreSQL.
-- Datas ISO 8601 validadas no ETL. Valores monetários em centavos inteiros.
CREATE TABLE IF NOT EXISTS departments (
 department_id INTEGER PRIMARY KEY, name TEXT NOT NULL,
 updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS employees (
 employee_id INTEGER PRIMARY KEY,
 department_id INTEGER NOT NULL REFERENCES departments(department_id),
 hired_on TEXT NOT NULL, ended_on TEXT,
 salary_cents INTEGER NOT NULL CHECK(salary_cents > 0),
 updated_at TEXT NOT NULL,
 CHECK(ended_on IS NULL OR ended_on > hired_on)
);
CREATE TABLE IF NOT EXISTS monthly_facts (
 employee_id INTEGER NOT NULL REFERENCES employees(employee_id),
 month TEXT NOT NULL,
 payroll_cents INTEGER NOT NULL CHECK(payroll_cents >= 0),
 scheduled_minutes INTEGER NOT NULL CHECK(scheduled_minutes >= 0),
 captured_minutes INTEGER NOT NULL CHECK(captured_minutes >= 0),
 productive_minutes INTEGER NOT NULL CHECK(productive_minutes >= 0),
 mapped INTEGER NOT NULL CHECK(mapped IN (0,1)),
 updated_at TEXT NOT NULL,
 PRIMARY KEY(employee_id,month),
 CHECK(productive_minutes <= captured_minutes),
 CHECK(captured_minutes <= scheduled_minutes),
 CHECK(mapped=1 OR captured_minutes=0)
);
CREATE INDEX IF NOT EXISTS ix_facts_month ON monthly_facts(month);
CREATE TABLE IF NOT EXISTS etl_batches (
 batch_name TEXT PRIMARY KEY, sha256 TEXT NOT NULL, loaded_at TEXT NOT NULL,
 changed_rows INTEGER NOT NULL
);
