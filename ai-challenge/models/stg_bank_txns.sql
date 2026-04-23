-- models/stg_bank_txns.sql
-- dbt-style staging model for bank settlement transactions.
-- TODO: replace with your cleaned staging query.

SELECT
    bank_ref,
    amount,
    txn_at,
    terminal_id,
    bank_code,
    CAST(txn_at AS DATE) AS txn_date
FROM raw_bank_txns
WHERE amount IS NOT NULL;
