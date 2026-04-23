-- models/rec_matched.sql
-- TODO: build the matched reconciliation set.
-- Rules:
--   - Exact match: same amount AND time diff <= 5 min
--   - Near match:  amount diff <= 100 IDR AND time diff <= 10 min
--   - Each invoice/bank txn used at most once (1:1)
--   - Exact matches win over near matches when both are possible
--
-- Hint: DuckDB supports ASOF joins and window functions. You can also do this
-- in Python after SELECTing both staging tables.

-- Placeholder: empty result
SELECT
    CAST(NULL AS VARCHAR) AS invoice_id,
    CAST(NULL AS VARCHAR) AS bank_ref,
    CAST(NULL AS DOUBLE)  AS amount,
    CAST(NULL AS VARCHAR) AS match_type,
    CAST(NULL AS DOUBLE)  AS amount_diff,
    CAST(NULL AS INTEGER) AS time_diff_seconds
WHERE 1 = 0;
