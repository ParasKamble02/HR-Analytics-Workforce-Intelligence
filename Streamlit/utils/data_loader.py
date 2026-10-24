import pandas as pd
from pathlib import Path

def load_data():
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir.parent / "data"

    csv_files = list(data_dir.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(
            "No CSV dataset found inside the data folder."
        )

    df = pd.read_csv(csv_files[0])

    #Clean column names
    df.columns = df.columns.str.strip()

    #Clean string columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()

    #Clean important columns
    if "Attrition" in df.columns:
        df["Attrition"] = (
            df["Attrition"]
            .astype(str)
            .str.strip()
            .str.title()
        )
    if "Department" in df.columns:
        df["Department"] = (
            df["Department"]
            .astype(str)
            .str.strip()
        )
    if "JobRole" in df.columns:
        df["JobRole"] = (
            df["JobRole"]
            .astype(str)
            .str.strip()
        )
    return df