"""
SATU Dental — Problem 2: EDC Bank File Reconciliation

Implement reconcile() below. See README.md for the full spec.
"""

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class ReconciliationResult:
    matched: List[Dict] = field(default_factory=list)
    near_matched: List[Dict] = field(default_factory=list)
    unmatched_invoices: List[Dict] = field(default_factory=list)
    unmatched_bank: List[Dict] = field(default_factory=list)


def reconcile(invoices: List[Dict], bank_txns: List[Dict]) -> ReconciliationResult:
    """
    Reconcile internal invoices against bank transactions.

    Rules:
      - Exact match: same amount AND time diff <= 5 minutes.
      - Near match:  amount diff <= 100 IDR AND time diff <= 10 minutes.
      - Each invoice / bank txn can be used at most once.
      - Exact matches are preferred over near matches.

    Returns a ReconciliationResult.
    """
    # TODO: implement
    return ReconciliationResult(
        matched=[],
        near_matched=[],
        unmatched_invoices=list(invoices),
        unmatched_bank=list(bank_txns),
    )
