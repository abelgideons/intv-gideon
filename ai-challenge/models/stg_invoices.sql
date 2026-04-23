-- models/stg_invoices.sql
-- dbt-style staging model for internal invoices.
-- TODO: replace with your cleaned staging query.
-- Rules:
--   - Drop rows where amount IS NULL
--   - Add paid_date column (DATE part of paid_at)
--   - Keep only columns needed downstream

SELECT
    invoice_id,
    amount,
    paid_at,
    clinic_id,
    CAST(paid_at AS DATE) AS paid_date
FROM raw_invoices
WHERE amount IS NOT NULL;
