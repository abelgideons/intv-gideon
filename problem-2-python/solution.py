import pandas as pd

def summarize(input_path: str) -> pd.DataFrame:
    
    # Step 1: Load CSV
    df = pd.read_csv(input_path)
    
    # Step 2: Deduplication appointment_id
    df = df.drop_duplicates(subset=['appointment_id'], keep='first')
    
    # Step 3: Normalize status lowercase
    df["status"] = df["status"].str.lower().str.strip()
    
    # Step 4: Parse appointment_date to datetime64
    df["appointment_date"] = pd.to_datetime(
        df["appointment_date"], errors="coerce"
    ).dt.date
    
    # Step 5: Coerce total_amount (fix utama)
    df["total_amount"] = (
        df["total_amount"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.strip()
        .replace(["", "None", "nan", "NULL"], "0")
    )
    
    df["total_amount"] = pd.to_numeric(
        df["total_amount"], errors="coerce"
    ).fillna(0)
    
    # Step 6: Aggregate per appointment_date, clinic_name
    def aggregate_val(group):
        return pd.Series({
            "completed_count": (group["status"] == "completed").sum(),
            "no_show_count": (group["status"] == "no_show").sum(),
            "cancelled_count": (group["status"] == "cancelled").sum(),
            "total_revenue": group.loc[
                group["status"] == "completed", "total_amount"
            ].sum()
        })
    
    result = (
        df.groupby(["appointment_date", "clinic_name"])
          .apply(aggregate_val)
          .reset_index()
    )
    
    # Step 7: Sort by appointment_date, clinic_name
    result = result.sort_values(by=["appointment_date", "clinic_name"])
    
    # Step 8: Reorder Column
    result = result[
        [
            "appointment_date",
            "clinic_name",
            "completed_count",
            "no_show_count",
            "cancelled_count",
            "total_revenue"
        ]
    ]
        
    return result
