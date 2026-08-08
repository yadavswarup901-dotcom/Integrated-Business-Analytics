
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
CLEAN = ROOT / "data" / "cleaned"
CLEAN.mkdir(parents=True, exist_ok=True)

def clean_sales():
    df = pd.read_csv(RAW / "sales.csv")
    df = df.drop_duplicates()
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    numeric = ["Quantity","Unit_Price","Discount","Sales","Profit"]
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df[numeric] = df[numeric].fillna(0)
    df["Region"] = df["Region"].fillna("Unknown")
    df["Category"] = df["Category"].fillna("Unknown")
    df["Product"] = df["Product"].fillna("Unknown")
    df.to_csv(CLEAN / "sales_cleaned.csv", index=False)
    return df

def clean_marketing():
    df = pd.read_csv(RAW / "marketing.csv")
    df = df.drop_duplicates()
    numeric = ["Spend","Impressions","Clicks","Conversions","Revenue"]
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df[numeric] = df[numeric].fillna(0)
    for col in ["Channel","Campaign"]:
        df[col] = df[col].fillna("Unknown")
    df["CTR"] = (df["Clicks"] / df["Impressions"].replace(0, pd.NA) * 100).fillna(0)
    df["Conversion_Rate"] = (df["Conversions"] / df["Clicks"].replace(0, pd.NA) * 100).fillna(0)
    df["ROI"] = ((df["Revenue"] - df["Spend"]) / df["Spend"].replace(0, pd.NA) * 100).fillna(0)
    df["CPC"] = (df["Spend"] / df["Clicks"].replace(0, pd.NA)).fillna(0)
    df.to_csv(CLEAN / "marketing_cleaned.csv", index=False)
    return df

def clean_hr():
    df = pd.read_csv(RAW / "hr.csv")
    df = df.drop_duplicates()
    numeric = ["Age","Years_At_Company","Salary","Job_Satisfaction","Workload_Level"]
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df[numeric] = df[numeric].fillna(df[numeric].median())
    for col in ["Department","Job_Role","Attrition"]:
        df[col] = df[col].fillna("Unknown")
    df.to_csv(CLEAN / "hr_cleaned.csv", index=False)
    return df

if __name__ == "__main__":
    clean_sales()
    clean_marketing()
    clean_hr()
    print("All datasets cleaned successfully.")
