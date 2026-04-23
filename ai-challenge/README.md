# AI-Assisted Development Challenge (30 min)

## Scenario

> "You're the first data engineer at SATU Dental. It's your first day. The finance team needs a **daily reconciliation pipeline** that matches internal invoices against bank EDC/ECR settlement files. You have Claude Code / Copilot / Cursor and 30 minutes. Build it."

This is very close to the Mage.ai reconciliation POC on your Bank Saqu resume. We want to see how you execute a greenfield pipeline **end-to-end with AI assistance**.

## What You're Building

A minimal but runnable reconciliation pipeline with 4 moving parts:

1. **Extract** — read `data/invoices.csv` and `data/bank_txns.csv`.
2. **Load** — load both raw CSVs into staging tables in DuckDB (local warehouse stand-in for BigQuery).
3. **Transform** — build dbt-style models:
   - `stg_invoices`, `stg_bank_txns` (cleaned staging)
   - `rec_matched` (exact + near matches)
   - `rec_exceptions` (unmatched on either side)
   - `rec_summary` (per-day totals: matched count, unmatched count, matched amount, exceptions amount)
4. **Orchestrate** — a simple Python DAG in `dag.py` that runs the 4 steps in order with logging and a retry decorator.

## Ground Rules

- You **must** use Claude Code / Copilot / Cursor — that's the point.
- Talk through your prompts and decisions as you work. We want to hear your thought process.
- Be honest about what the AI wrote vs. what you wrote.
- Finish with a working `python dag.py` command that executes the whole pipeline and prints a summary.
- Commit frequently.

## Starter Files

```
ai-challenge/
├── README.md               <- you are here
├── pipeline.py             <- Python extract/load/transform/reconcile skeleton
├── dag.py                  <- simple DAG runner with retry decorator
├── schema.sql              <- DuckDB DDL for staging + reconciliation tables
├── models/
│   ├── stg_invoices.sql    <- dbt-style staging model (placeholder)
│   ├── stg_bank_txns.sql
│   ├── rec_matched.sql
│   └── rec_summary.sql
├── data/
│   ├── invoices.csv        <- sample internal invoices
│   └── bank_txns.csv       <- sample bank settlements
└── requirements.txt
```

## How to Run

```bash
pip install -r requirements.txt
python dag.py
```

Expected output at the end:
```
[pipeline] extract OK
[pipeline] load OK
[pipeline] transform OK
[pipeline] summary: matched=X near_matched=Y exceptions=Z total_matched_amount=...
```

## Tips

- Start small. Get `extract` + `load` working first before touching `transform`.
- Use DuckDB's `read_csv_auto` to load staging data quickly — it's built in.
- The data files are intentionally messy — expect NULLs, slight amount diffs (fees), and duplicates.
- You don't need full dbt installed — the `models/` SQL files are placeholders; you can either `INSTALL dbt` or just execute the SQL against DuckDB directly. Pick whichever is faster.
