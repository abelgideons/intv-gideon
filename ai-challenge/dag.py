"""
SATU Dental — AI-Assisted Challenge
Minimal DAG runner.

This is a very small orchestrator stand-in for Airflow/Mage. It runs the
pipeline steps in order, with a retry decorator and simple logging.
"""

from __future__ import annotations

import functools
import logging
import sys
import time
from typing import Callable

from pipeline import PipelineConfig, extract, load, transform, reconcile

logger = logging.getLogger("dag")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("[%(name)s] %(message)s"))
if not logger.handlers:
    logger.addHandler(handler)


def retry(max_attempts: int = 3, delay_seconds: float = 1.0):
    """Retry decorator: re-run the step on failure up to max_attempts times."""

    def decorator(fn: Callable):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as exc:  # noqa: BLE001
                    last_exc = exc
                    logger.warning(
                        "step %s failed attempt %s/%s: %s",
                        fn.__name__,
                        attempt,
                        max_attempts,
                        exc,
                    )
                    if attempt < max_attempts:
                        time.sleep(delay_seconds)
            logger.error("step %s exhausted retries", fn.__name__)
            raise last_exc  # type: ignore[misc]

        return wrapper

    return decorator


def run_dag(cfg: PipelineConfig | None = None) -> dict:
    cfg = cfg or PipelineConfig()

    steps = [
        ("extract", retry(max_attempts=2)(extract)),
        ("load", retry(max_attempts=3)(load)),
        ("transform", retry(max_attempts=2)(transform)),
        ("reconcile", retry(max_attempts=2)(reconcile)),
    ]

    summary: dict = {}
    for name, fn in steps:
        logger.info("running step: %s", name)
        result = fn(cfg)
        if name == "reconcile" and isinstance(result, dict):
            summary = result
    logger.info("dag finished")
    return summary


if __name__ == "__main__":
    try:
        run_dag()
    except NotImplementedError as e:
        logger.error("pipeline has unimplemented steps: %s", e)
        sys.exit(1)
