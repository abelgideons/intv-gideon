# Problem 2 — Python: EDC Bank File Reconciliation (20 min)

## Context

SATU Dental receives daily settlement files from banks (BCA, BRI, Mandiri) via SFTP. We need to reconcile each bank's transactions against our internal invoice records to identify:

1. **Matched** — bank transactions that correspond exactly to an invoice.
2. **Near-matched** — bank transactions that match within tolerance (e.g., bank fees deducted, or a few minutes of clock drift).
3. **Unmatched invoices** — invoices with no corresponding bank transaction.
4. **Unmatched bank transactions** — bank transactions with no corresponding invoice.

You'll build the match engine.

## Task

Implement `reconcile(invoices, bank_txns)` in `solution.py`.

### Signature

```python
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class ReconciliationResult:
    matched: List[Dict]
    near_matched: List[Dict]
    unmatched_invoices: List[Dict]
    unmatched_bank: List[Dict]

def reconcile(invoices: List[Dict], bank_txns: List[Dict]) -> ReconciliationResult:
    ...
```

### Input shape

```python
invoices = [
    {"invoice_id": "INV-001", "amount": 500000.00, "paid_at": "2026-04-01 10:30:00", "clinic_id": 1},
    ...
]

bank_txns = [
    {"bank_ref": "BCA20260401001", "amount": 500000.00, "txn_at": "2026-04-01 10:31:12", "terminal_id": "TERM-1"},
    ...
]
```

### Matching rules

1. **Exact match:** `amount` is identical AND `abs(paid_at - txn_at) <= 5 minutes`.
2. **Near match:** `abs(amount - bank_amount) <= 100` IDR (bank fees) AND `abs(paid_at - txn_at) <= 10 minutes`. Each near-matched dict should include `amount_diff` and `time_diff_seconds`.
3. Each invoice and bank transaction must match **at most once** (1:1).
4. **Exact matches take priority** — do exact matching first, then fuzzy match over the leftovers.
5. When multiple near-matches are possible, pick the one with the smallest combined `(amount_diff, time_diff)`.

### Return shape

A `ReconciliationResult` dataclass with four lists:
- `matched`: `[{"invoice": {...}, "bank_txn": {...}}, ...]`
- `near_matched`: `[{"invoice": {...}, "bank_txn": {...}, "amount_diff": X, "time_diff_seconds": Y}, ...]`
- `unmatched_invoices`: `[{...}, ...]`
- `unmatched_bank`: `[{...}, ...]`

## How to Run

```bash
pip install -r requirements.txt
pytest -v
```

All tests are in `test_solution.py`. They will fail until you implement `reconcile`.

## Evaluation

- Correctness across all 8 tests.
- Uses an index (hash map) for the exact-match pass — not nested loops.
- Correctly enforces 1:1 matching.
- Exact match is preferred over near match when the same bank transaction could serve either.
- Handles empty inputs and timestamp parsing cleanly.
- Readable, idiomatic Python. Type hints encouraged.
