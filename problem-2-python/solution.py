import pandas as pd

def summarize(input_path: str) -> pd.DataFrame:
    df = pd.read_csv(input_path)

    # Deduplicate
    df = df.drop_duplicates(subset=["appointment_id"], keep="first")

    # Normalize status
    df["status"] = df["status"].str.lower().str.strip()

    # Parse date
    df["appointment_date"] = pd.to_datetime(df["appointment_date"], errors="coerce").dt.date

    # Clean total_amount
    df["total_amount"] = (
        df["total_amount"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce").fillna(0)

    # Aggregate 
    result = (
        df.groupby(["appointment_date", "clinic_name"])
        .agg(
            completed_count=("status", lambda x: (x == "completed").sum()),
            no_show_count=("status", lambda x: (x == "no_show").sum()),
            cancelled_count=("status", lambda x: (x == "cancelled").sum()),
            total_revenue=("total_amount", lambda x: x[df.loc[x.index, "status"] == "completed"].sum()),
        )
        .reset_index()
    )

    # Sort
    result = result.sort_values(by=["appointment_date", "clinic_name"])

    return result[
        [
            "appointment_date",
            "clinic_name",
            "completed_count",
            "no_show_count",
            "cancelled_count",
            "total_revenue",
        ]
    ]



# """
# SATU Dental — Problem 2: Appointment Data Cleanup & Daily Summary

# Implement summarize() below. See README.md for the full spec.
# """

# import pandas as pd


# def summarize(input_path: str) -> pd.DataFrame:
#     """
#     Load a messy appointments CSV, clean it, and return a daily
#     revenue summary per clinic.

#     Output columns (in order):
#         appointment_date, clinic_name,
#         completed_count, no_show_count, cancelled_count,
#         total_revenue
#     """
#     # TODO: implement
#     raise NotImplementedError
