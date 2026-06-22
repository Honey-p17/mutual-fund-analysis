import pandas as pd
from pathlib import Path

data_path=Path("Data/raw")
# df =pd.read_csv("")
csv_files = list(data_path.glob("*.csv"))
print(f"Found {len(csv_files)} CSV files")

# for file in csv_files:

#     print("file",file.name)

#     df=pd.read_csv(file)

#     print("\nshape")
#     print(df.shape)

#     print("\n data types")
#     print(df.dtypes)

#     print("\n head")
#     print(df.head())

# Load fund master dataset
fund_master = pd.read_csv("data/raw/01_fund_master.csv")

print("\nFund Houses:")
print(fund_master["fund_house"].unique())

print("\nCategories:")
print(fund_master["category"].unique())

print("\nSub Categories:")
print(fund_master["sub_category"].unique())

print("\nRisk Grades:")
print(fund_master["risk_category"].unique())

# Read NAV history file
nav_history = pd.read_csv("data/raw/02_nav_history.csv")

# Get unique AMFI codes from both files
fund_master_codes = set(fund_master["amfi_code"])
nav_history_codes = set(nav_history["amfi_code"])

# Find codes that are in fund master but not in NAV history
missing_codes = fund_master_codes - nav_history_codes

print("\nAMFI Code Validation")
print("Total codes in Fund Master:", len(fund_master_codes))
print("Total codes in NAV History:", len(nav_history_codes))

if len(missing_codes) == 0:
    print("All AMFI codes are present in NAV History.")
else:
    print("Missing AMFI Codes:")
    print(missing_codes)