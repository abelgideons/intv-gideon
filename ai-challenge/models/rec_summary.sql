-- models/rec_summary.sql
-- TODO: aggregate reconciliation output into a daily summary.
-- Columns expected:
--   rec_date, matched_count, near_matched_count, exceptions_count,
--   matched_amount, exceptions_amount

SELECT
    CAST(NULL AS DATE)    AS rec_date,
    CAST(0 AS INTEGER)    AS matched_count,
    CAST(0 AS INTEGER)    AS near_matched_count,
    CAST(0 AS INTEGER)    AS exceptions_count,
    CAST(0 AS DOUBLE)     AS matched_amount,
    CAST(0 AS DOUBLE)     AS exceptions_amount
WHERE 1 = 0;
