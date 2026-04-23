"""
SATU Dental — AI-Assisted Challenge
Reconciliation pipeline skeleton.

You will implement the extract / load / transform / reconcile functions below
with the help of Claude Code / Copilot. Each function currently raises
NotImplementedError and is wired up by dag.py.

Target warehouse: DuckDB (local stand-in for BigQuery).
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import duckdb

logger = logging.getLogger("pipeline")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("[%(name)s] %(message)s"))
if not logger.handlers:
    logger.addHandler(handler)

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = BASE_DIR / "warehouse.duckdb"
SCHEMA_SQL = BASE_DIR / "schema.sql"


@dataclass
class PipelineConfig:
    invoices_csv: Path = DATA_DIR / "invoices.csv"
    bank_txns_csv: Path = DATA_DIR / "bank_txns.csv"
    db_path: Path = DB_PATH
    exact_time_window_seconds: int = 5 * 60
    near_time_window_seconds: int = 10 * 60
    near_amount_tolerance: float = 100.00


def get_connection(db_path: Path) -> duckdb.DuckDBPyConnection:
    """Return a DuckDB connection. Initializes the schema if needed."""
    con = duckdb.connect(str(db_path))
    with open(SCHEMA_SQL) as f:
        con.execute(f.read())
    return con


def extract(cfg: PipelineConfig) -> None:
    """
    Step 1: Extract — verify source files exist.

    For this challenge, extract is minimal: we just confirm the CSVs are
    present. In a real pipeline this would pull from SFTP, an API, etc.
    """
    logger.info("extract: checking source files")
    if not cfg.invoices_csv.exists():
        raise FileNotFoundError(f"Missing {cfg.invoices_csv}")
    if not cfg.bank_txns_csv.exists():
        raise FileNotFoundError(f"Missing {cfg.bank_txns_csv}")
    logger.info("extract OK")


def load(cfg: PipelineConfig) -> None:
    """
    Step 2: Load — read CSVs into raw_invoices and raw_bank_txns.

    TODO: Use DuckDB's read_csv_auto to load both CSVs into the raw tables.
    Truncate existing rows first for idempotency.
    """
    logger.info("load: loading raw tables")
    # TODO: implement
    raise NotImplementedError("TODO: load raw CSVs into DuckDB")


def transform(cfg: PipelineConfig) -> None:
    """
    Step 3: Transform — build stg_invoices and stg_bank_txns from raw.

    TODO: Execute the staging model SQL files in models/ (or inline SQL).
    Drop invoices with NULL amount. Add paid_date / txn_date columns.
    """
    logger.info("transform: building staging models")
    # TODO: implement
    raise NotImplementedError("TODO: build staging tables")


def reconcile(cfg: PipelineConfig) -> dict:
    """
    Step 4: Reconcile — build rec_matched, rec_exceptions, rec_summary.

    TODO:
      - Exact match: same amount AND abs(time diff) <= exact_time_window_seconds
      - Near match:  abs(amount_diff) <= near_amount_tolerance AND
                     abs(time_diff) <= near_time_window_seconds
      - 1:1: each invoice/bank txn at most once
      - Populate rec_matched, rec_exceptions, rec_summary
      - Return a dict summary for logging

    Hint: You can do this entirely in SQL (DuckDB supports window functions and
    ASOF joins), or in Python after fetching both tables. Pick whichever you
    can defend.
    """
    logger.info("reconcile: matching invoices to bank transactions")
    # TODO: implement
    raise NotImplementedError("TODO: build reconciliation output")


def run_pipeline(cfg: Optional[PipelineConfig] = None) -> dict:
    """End-to-end pipeline runner."""
    cfg = cfg or PipelineConfig()
    extract(cfg)
    load(cfg)
    transform(cfg)
    summary = reconcile(cfg)
    logger.info(
        "summary: matched=%s near_matched=%s exceptions=%s total_matched_amount=%s",
        summary.get("matched_count", 0),
        summary.get("near_matched_count", 0),
        summary.get("exceptions_count", 0),
        summary.get("matched_amount", 0),
    )
    return summary


if __name__ == "__main__":
    run_pipeline()
