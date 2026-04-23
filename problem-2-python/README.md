# Problem 2 — Pandas: Appointment Data Cleanup & Daily Summary (20 min)

## Context

An analyst at SATU Dental dropped a raw CSV export of appointments on your desk and asked for a **daily revenue summary per clinic**. The export is messy:

- Duplicate rows (same `appointment_id` appears more than once).
- `total_amount` is sometimes a plain number, sometimes a string with commas (`"1,250,000.00"`), sometimes NULL/empty.
- `status` is inconsistent case: `"completed"`, `"COMPLETED"`, `"Completed"`.
- `appointment_date` is a string (`"2026-04-01"`) — not yet parsed.

Build a small pandas pipeline that cleans the data and produces the daily summary.

## Task

Implement `summarize(input_path: str) -> pd.DataFrame` in `solution.py`.

### Steps

1. **Load** the CSV at `input_path`.
2. **Deduplicate** on `appointment_id` (keep the first occurrence).
3. **Normalize `status`** to lowercase.
4. **Parse `appointment_date`** into a proper `datetime64` (date only).
5. **Coerce `total_amount`** to numeric — strip commas, treat blanks/NULL as 0.
6. **Aggregate** per `(appointment_date, clinic_name)`:
   - `completed_count` — number of appointments with status `"completed"`
   - `no_show_count` — number with status `"no_show"`
   - `cancelled_count` — number with status `"cancelled"`
   - `total_revenue` — sum of `total_amount` for `"completed"` appointments only
7. **Sort** the result by `appointment_date`, then `clinic_name`.
8. **Return** a DataFrame with these columns in this order:
   `["appointment_date", "clinic_name", "completed_count", "no_show_count", "cancelled_count", "total_revenue"]`

### Input columns

| Column            | Type (raw)     |
|-------------------|----------------|
| appointment_id    | int            |
| patient_id        | int            |
| clinic_name       | str            |
| appointment_date  | str (YYYY-MM-DD) |
| status            | str (mixed case) |
| total_amount      | str / number / NULL |

## How to Run

```bash
pip install -r requirements.txt
pytest -v
```

The tests use an in-memory sample dataset and a small CSV fixture in `data/appointments.csv`.

Write your solution in `solution.py`.
