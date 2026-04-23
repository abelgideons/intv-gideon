# Problem 1 — SQL: Patient First-vs-Return Visit Analysis (15 min)

## Context
SATU Dental wants to understand first-visit vs return-visit patterns per clinic per month, to measure patient retention across our clinics in Jakarta.

## Schema

```sql
CREATE TABLE patients (
    patient_id INT PRIMARY KEY,
    full_name VARCHAR(200),
    created_at TIMESTAMP
);

CREATE TABLE clinics (
    clinic_id INT PRIMARY KEY,
    clinic_name VARCHAR(100),
    city VARCHAR(100)
);

CREATE TABLE appointments (
    appointment_id INT PRIMARY KEY,
    patient_id INT,
    clinic_id INT,
    appointment_date DATE,
    status VARCHAR(20),   -- 'completed', 'no_show', 'cancelled'
    total_amount NUMERIC(12,2)
);
```

Full seed data is in `seed_data.sql`. It contains ~25 appointments across 6 patients, 3 clinics, spanning Jan–Mar 2026, including no-shows, cancellations, a duplicate same-day appointment for one patient, and a NULL in `total_amount`.

## Task

Write a single SQL query that returns, for each (clinic, month):

| Column                  | Description |
|-------------------------|-------------|
| `clinic_name`           | Clinic name |
| `month`                 | First day of the month (DATE) |
| `total_completed_visits`| Count of completed appointments (after dedup — see rules) |
| `unique_patients`       | Distinct patients who had at least one completed visit that month |
| `first_time_patients`   | Patients whose first-ever completed visit **at this clinic** was this month |
| `returning_patients`    | `unique_patients - first_time_patients` |
| `retention_rate_pct`    | `returning_patients * 100.0 / unique_patients`, rounded to 2 decimals (NULL-safe) |
| `total_revenue`         | Sum of `total_amount` for completed visits (NULL treated as 0) |

Order by `clinic_name`, `month`.

## Rules

1. **Exclude** appointments with status `no_show` or `cancelled`.
2. **Same-day duplicates** for a patient at the same clinic on the same date should count as **one visit**. Keep the one with the highest `total_amount` (NULLs rank last).
3. **"First time at this clinic"** is scoped per clinic — a patient can be first-time at Clinic A in February and returning at Clinic B in the same month.
4. **Treat NULL `total_amount` as 0** when summing revenue.
5. **Retention rate**: guard against divide-by-zero and return a 2-decimal numeric value.

## Expected Result

| clinic_name       | month      | total_completed_visits | unique_patients | first_time_patients | returning_patients | retention_rate_pct | total_revenue |
|-------------------|------------|------------------------|-----------------|---------------------|--------------------|--------------------|---------------|
| Kemang Dental     | 2026-01-01 | 3                      | 3               | 3                   | 0                  | 0.00               | 1450000.00    |
| Kemang Dental     | 2026-02-01 | 2                      | 2               | 0                   | 2                  | 100.00             | 900000.00     |
| Kemang Dental     | 2026-03-01 | 2                      | 2               | 1                   | 1                  | 50.00              | 1100000.00    |
| PIK Dental Center | 2026-01-01 | 2                      | 2               | 2                   | 0                  | 0.00               | 850000.00     |
| PIK Dental Center | 2026-02-01 | 2                      | 1               | 0                   | 1                  | 100.00             | 750000.00     |
| Senopati Smile    | 2026-02-01 | 2                      | 2               | 2                   | 0                  | 0.00               | 1200000.00    |
| Senopati Smile    | 2026-03-01 | 1                      | 1               | 0                   | 1                  | 100.00             | 650000.00     |

## Key Things to Note

- Exclude `no_show` and `cancelled` **before** any aggregation.
- Collapse same-day duplicates per (patient, clinic, date) — `ROW_NUMBER() OVER (PARTITION BY patient_id, clinic_id, appointment_date ORDER BY total_amount DESC NULLS LAST)` and keep row 1.
- "First-time at this clinic" is **per-clinic**, not global. Use `MIN(appointment_date) OVER (PARTITION BY patient_id, clinic_id)` on the deduped completed visits.
- Use `COALESCE(total_amount, 0)` for revenue.
- Guard `retention_rate_pct` against divide-by-zero.

## How to Run

We've targeted **PostgreSQL 15+** syntax but any major dialect with window functions works. To run locally:

```bash
psql -U postgres -d test -f seed_data.sql
psql -U postgres -d test -f solution.sql
```

Or use any online Postgres sandbox.

Write your solution in `solution.sql`.
