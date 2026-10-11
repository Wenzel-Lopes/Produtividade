-- PostgreSQL 16+. Exatamente uma linha por mês e departamento.
-- Desligamento é o primeiro dia inativo. Headcount usa o último dia do mês.
CREATE OR REPLACE VIEW vw_kpis_monthly AS
WITH months AS (
 SELECT DISTINCT month::date AS month FROM monthly_facts
), population AS (
 SELECT m.month,d.department_id,d.name AS department,
 COUNT(e.employee_id) FILTER (WHERE e.hired_on::date < m.month
  AND (e.ended_on IS NULL OR e.ended_on::date >= m.month)) AS opening_headcount,
 COUNT(e.employee_id) FILTER (WHERE e.hired_on::date < m.month + INTERVAL '1 month'
  AND (e.ended_on IS NULL OR e.ended_on::date >= m.month + INTERVAL '1 month')) AS headcount,
 COUNT(e.employee_id) FILTER (WHERE e.hired_on::date >= m.month
  AND e.hired_on::date < m.month + INTERVAL '1 month') AS hires,
 COUNT(e.employee_id) FILTER (WHERE e.ended_on::date >= m.month
  AND e.ended_on::date < m.month + INTERVAL '1 month') AS exits
 FROM months m CROSS JOIN departments d
 LEFT JOIN employees e ON e.department_id=d.department_id
 GROUP BY m.month,d.department_id,d.name
), activity AS (
 SELECT f.month::date AS month,e.department_id,
 SUM(f.payroll_cents)/100.0 AS payroll_brl,
 SUM(f.scheduled_minutes) AS scheduled_minutes,
 SUM(f.captured_minutes) AS captured_minutes,
 SUM(f.productive_minutes) AS productive_minutes,
 SUM(f.mapped) AS mapped_employees,COUNT(*) AS eligible_employees
 FROM monthly_facts f JOIN employees e USING(employee_id)
 GROUP BY f.month,e.department_id
)
SELECT p.*, COALESCE(a.payroll_brl,0) AS payroll_brl,
 p.exits/NULLIF((p.opening_headcount+p.headcount)/2.0,0) AS turnover,
 a.mapped_employees::numeric/NULLIF(a.eligible_employees,0) AS mapping_coverage,
 a.productive_minutes::numeric/NULLIF(a.captured_minutes,0) AS observed_activity_ratio,
 a.captured_minutes::numeric/NULLIF(a.scheduled_minutes,0) AS collection_coverage,
 a.eligible_employees,a.mapped_employees,a.scheduled_minutes,a.captured_minutes,a.productive_minutes
FROM population p LEFT JOIN activity a USING(month,department_id);

-- Exemplo: variação mensal de folha, sem multiplicação por joins de pessoas.
-- SELECT *, payroll_brl-LAG(payroll_brl) OVER
-- (PARTITION BY department_id ORDER BY month) AS payroll_delta_brl
-- FROM vw_kpis_monthly ORDER BY department_id,month;
