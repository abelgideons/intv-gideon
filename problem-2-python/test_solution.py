"""Tests for Problem 2 — summarize()."""

import os
import pandas as pd

from solution import summarize

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "appointments.csv")


def test_returns_dataframe_with_expected_columns():
    df = summarize(DATA_PATH)
    expected = [
        "appointment_date",
        "clinic_name",
        "completed_count",
        "no_show_count",
        "cancelled_count",
        "total_revenue",
    ]
    assert list(df.columns) == expected


def test_deduplication():
    df = summarize(DATA_PATH)
    # appointment_id=1 is duplicated in the CSV; Kemang 2026-04-01 should
    # still only show 2 completed visits (ids 1 and 2), not 3.
    row = df[
        (df["appointment_date"] == pd.Timestamp("2026-04-01"))
        & (df["clinic_name"] == "Kemang Dental")
    ].iloc[0]
    assert row["completed_count"] == 2


def test_status_case_normalization():
    df = summarize(DATA_PATH)
    # 2026-04-02 Kemang has one "Completed" and one "NO_SHOW" → mixed case
    row = df[
        (df["appointment_date"] == pd.Timestamp("2026-04-02"))
        & (df["clinic_name"] == "Kemang Dental")
    ].iloc[0]
    assert row["completed_count"] == 1
    assert row["no_show_count"] == 1


def test_total_amount_parsing_and_null_handling():
    df = summarize(DATA_PATH)
    # 2026-04-01 Kemang: completed 500000 + 450000 = 950000; no_show row has
    # NULL amount and must not contribute to revenue.
    row = df[
        (df["appointment_date"] == pd.Timestamp("2026-04-01"))
        & (df["clinic_name"] == "Kemang Dental")
    ].iloc[0]
    assert row["total_revenue"] == 950000


def test_comma_formatted_amount():
    df = summarize(DATA_PATH)
    # 2026-04-03 Senopati: "2,500,000.00" + NULL completed = 2_500_000
    row = df[
        (df["appointment_date"] == pd.Timestamp("2026-04-03"))
        & (df["clinic_name"] == "Senopati Smile")
    ].iloc[0]
    assert row["total_revenue"] == 2_500_000
    assert row["completed_count"] == 2


def test_sorted_by_date_then_clinic():
    df = summarize(DATA_PATH)
    dates = df["appointment_date"].tolist()
    assert dates == sorted(dates)
    for date in df["appointment_date"].unique():
        clinics = df[df["appointment_date"] == date]["clinic_name"].tolist()
        assert clinics == sorted(clinics)


def test_cancelled_counted_separately():
    df = summarize(DATA_PATH)
    # 2026-04-01 PIK: 1 completed + 1 cancelled
    row = df[
        (df["appointment_date"] == pd.Timestamp("2026-04-01"))
        & (df["clinic_name"] == "PIK Dental Center")
    ].iloc[0]
    assert row["completed_count"] == 1
    assert row["cancelled_count"] == 1
    assert row["no_show_count"] == 0
