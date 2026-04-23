-- SATU Dental — Reconciliation pipeline schema (DuckDB)
-- This file defines the raw landing tables and the reconciliation output tables.

-- ===== Raw landing =====

CREATE TABLE IF NOT EXISTS raw_invoices (
    invoice_id      VARCHAR,
    amount          DOUBLE,
    paid_at         TIMESTAMP,
    clinic_id       INTEGER,
    payment_method  VARCHAR,
    loaded_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS raw_bank_txns (
    bank_ref        VARCHAR,
    amount          DOUBLE,
    txn_at          TIMESTAMP,
    terminal_id     VARCHAR,
    bank_code       VARCHAR,
    loaded_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===== Staging (to be built via dbt-style models) =====

CREATE TABLE IF NOT EXISTS stg_invoices (
    invoice_id      VARCHAR,
    amount          DOUBLE,
    paid_at         TIMESTAMP,
    clinic_id       INTEGER,
    paid_date       DATE
);

CREATE TABLE IF NOT EXISTS stg_bank_txns (
    bank_ref        VARCHAR,
    amount          DOUBLE,
    txn_at          TIMESTAMP,
    terminal_id     VARCHAR,
    bank_code       VARCHAR,
    txn_date        DATE
);

-- ===== Reconciliation output =====

CREATE TABLE IF NOT EXISTS rec_matched (
    invoice_id      VARCHAR,
    bank_ref        VARCHAR,
    amount          DOUBLE,
    match_type      VARCHAR,   -- 'exact' or 'near'
    amount_diff     DOUBLE,
    time_diff_seconds INTEGER,
    reconciled_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS rec_exceptions (
    source          VARCHAR,   -- 'invoice' or 'bank'
    ref_id          VARCHAR,   -- invoice_id or bank_ref
    amount          DOUBLE,
    event_at        TIMESTAMP,
    reason          VARCHAR,
    reconciled_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS rec_summary (
    rec_date                DATE,
    matched_count           INTEGER,
    near_matched_count      INTEGER,
    exceptions_count        INTEGER,
    matched_amount          DOUBLE,
    exceptions_amount       DOUBLE,
    built_at                TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
