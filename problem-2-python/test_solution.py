"""
SATU Dental — Problem 2 pytest suite.
Run with: pytest -v
"""

import time
import random
from solution import reconcile, ReconciliationResult


def _inv(invoice_id, amount, paid_at, clinic_id=1):
    return {
        "invoice_id": invoice_id,
        "amount": amount,
        "paid_at": paid_at,
        "clinic_id": clinic_id,
    }


def _txn(bank_ref, amount, txn_at, terminal_id="TERM-1"):
    return {
        "bank_ref": bank_ref,
        "amount": amount,
        "txn_at": txn_at,
        "terminal_id": terminal_id,
    }


def test_perfect_match():
    """Two invoices, two bank txns, all exact."""
    invoices = [
        _inv("INV-001", 500000.00, "2026-04-01 10:30:00"),
        _inv("INV-002", 150000.00, "2026-04-01 11:05:00"),
    ]
    txns = [
        _txn("BCA001", 500000.00, "2026-04-01 10:31:00"),
        _txn("BCA002", 150000.00, "2026-04-01 11:06:00"),
    ]
    r = reconcile(invoices, txns)
    assert isinstance(r, ReconciliationResult)
    assert len(r.matched) == 2
    assert len(r.near_matched) == 0
    assert len(r.unmatched_invoices) == 0
    assert len(r.unmatched_bank) == 0
    matched_ids = {m["invoice"]["invoice_id"] for m in r.matched}
    assert matched_ids == {"INV-001", "INV-002"}


def test_near_match_amount():
    """Fee-adjusted match within IDR 100."""
    invoices = [_inv("INV-001", 500000.00, "2026-04-01 10:30:00")]
    txns = [_txn("BCA001", 499950.00, "2026-04-01 10:32:00")]
    r = reconcile(invoices, txns)
    assert len(r.matched) == 0
    assert len(r.near_matched) == 1
    nm = r.near_matched[0]
    assert nm["invoice"]["invoice_id"] == "INV-001"
    assert nm["bank_txn"]["bank_ref"] == "BCA001"
    assert nm["amount_diff"] == 50.00
    assert nm["time_diff_seconds"] == 120


def test_unmatched_both_sides():
    """Invoice with no bank, bank with no invoice."""
    invoices = [_inv("INV-001", 500000.00, "2026-04-01 10:30:00")]
    txns = [_txn("BCA999", 999000.00, "2026-04-01 15:00:00")]
    r = reconcile(invoices, txns)
    assert len(r.matched) == 0
    assert len(r.near_matched) == 0
    assert len(r.unmatched_invoices) == 1
    assert len(r.unmatched_bank) == 1
    assert r.unmatched_invoices[0]["invoice_id"] == "INV-001"
    assert r.unmatched_bank[0]["bank_ref"] == "BCA999"


def test_time_window_too_far():
    """Same amount but time delta > 10 min → unmatched."""
    invoices = [_inv("INV-001", 500000.00, "2026-04-01 10:30:00")]
    txns = [_txn("BCA001", 500000.00, "2026-04-01 11:00:00")]  # 30 min later
    r = reconcile(invoices, txns)
    assert len(r.matched) == 0
    assert len(r.near_matched) == 0
    assert len(r.unmatched_invoices) == 1
    assert len(r.unmatched_bank) == 1


def test_duplicate_prevention():
    """Two invoices with same amount+time, only one bank txn → 1 matched, 1 unmatched."""
    invoices = [
        _inv("INV-001", 500000.00, "2026-04-01 10:30:00"),
        _inv("INV-002", 500000.00, "2026-04-01 10:30:30"),
    ]
    txns = [_txn("BCA001", 500000.00, "2026-04-01 10:30:15")]
    r = reconcile(invoices, txns)
    assert len(r.matched) == 1
    assert len(r.unmatched_invoices) == 1
    assert len(r.unmatched_bank) == 0


def test_exact_preferred_over_near():
    """One bank txn could match two invoices (one exact, one near) → exact wins."""
    invoices = [
        _inv("INV-EXACT", 500000.00, "2026-04-01 10:30:00"),
        _inv("INV-NEAR",  500050.00, "2026-04-01 10:31:00"),
    ]
    txns = [_txn("BCA001", 500000.00, "2026-04-01 10:30:30")]
    r = reconcile(invoices, txns)
    assert len(r.matched) == 1
    assert r.matched[0]["invoice"]["invoice_id"] == "INV-EXACT"
    assert len(r.near_matched) == 0  # no bank txn left
    # INV-NEAR should end up unmatched
    unmatched_ids = {i["invoice_id"] for i in r.unmatched_invoices}
    assert "INV-NEAR" in unmatched_ids


def test_empty_inputs():
    """Empty inputs should return empty lists."""
    r = reconcile([], [])
    assert r.matched == []
    assert r.near_matched == []
    assert r.unmatched_invoices == []
    assert r.unmatched_bank == []


def test_large_batch():
    """100 invoices + 100 bank txns — correctness + reasonable runtime (< 2s)."""
    random.seed(42)
    invoices = []
    txns = []
    for i in range(100):
        amount = round(random.uniform(50000, 1000000), 2)
        minute = i
        paid_at = f"2026-04-01 {10 + minute // 60:02d}:{minute % 60:02d}:00"
        invoices.append(_inv(f"INV-{i:04d}", amount, paid_at))
        txns.append(_txn(f"BCA{i:04d}", amount, paid_at))

    start = time.time()
    r = reconcile(invoices, txns)
    elapsed = time.time() - start

    assert len(r.matched) == 100
    assert len(r.near_matched) == 0
    assert len(r.unmatched_invoices) == 0
    assert len(r.unmatched_bank) == 0
    assert elapsed < 2.0, f"Took {elapsed:.2f}s — should be well under 2s"
