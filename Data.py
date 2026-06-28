import pandas as pd

# ── 1. Load raw data ─────────────────────────────────────────
df = pd.read_csv('C:/Portfolio/car_prices.csv')

print("=== Raw Data ===")
print(f"Rows: {len(df)}")
print(f"Columns: {list(df.columns)}")
print()
print(df.head(3))
print()

# ── 2. Check missing values ──────────────────────────────────
print("=== Missing Values ===")
print(df.isnull().sum())
print()

# ── 3. Standardize column names (lowercase, underscores) ─────
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
print("=== Cleaned Column Names ===")
print(list(df.columns))
print()

# ── 4. Remove duplicate rows ─────────────────────────────────
before = len(df)
df = df.drop_duplicates()
print(f"Duplicate rows removed: {before - len(df)}")

# ── 5. Handle missing values in key numeric columns ──────────
# sellingprice: drop rows where selling price is missing
df = df.dropna(subset=['sellingprice'])

# odometer: fill missing with median
df['odometer'] = df['odometer'].fillna(df['odometer'].median())

print(f"Rows after cleaning: {len(df)}")
print()

# ── 6. Parse and extract date fields ────────────────────────
df['saledate'] = pd.to_datetime(df['saledate'], errors='coerce', utc=True)
df['saledate'] = df['saledate'].dt.tz_localize(None)
df['sale_year']       = df['saledate'].dt.year
df['sale_month']      = df['saledate'].dt.month
df['sale_month_name'] = df['saledate'].dt.strftime('%b')

# ── 7. Remove price outliers (selling price < $100) ──────────
before = len(df)
df = df[df['sellingprice'] >= 100]
print(f"Outlier rows removed: {before - len(df)}")

# ── 8. Add calculated fields ─────────────────────────────────
# Vehicle age at time of sale
df['car_age'] = df['sale_year'] - df['year']

# Price vs MMR market reference (positive = sold above market)
df['price_vs_mmr_pct'] = (
    (df['sellingprice'] - df['mmr']) / df['mmr'] * 100
).round(2)

# ── 9. Clean text fields ─────────────────────────────────────
for col in ['make', 'model', 'trim', 'body', 'transmission',
            'color', 'interior', 'condition', 'state']:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip().str.title()

# Map state abbreviations to full names
state_map = {
    'Ca': 'California', 'Fl': 'Florida',   'Tx': 'Texas',
    'Pa': 'Pennsylvania','Ga': 'Georgia',   'Nj': 'New Jersey',
    'Tn': 'Tennessee',   'Il': 'Illinois',  'Oh': 'Ohio',
    'Mo': 'Missouri',    'Mi': 'Michigan',  'Mn': 'Minnesota',
    'Nc': 'North Carolina','Nv': 'Nevada',  'Va': 'Virginia'
}
df['state'] = df['state'].map(state_map).fillna(df['state'])

# ── 10. Export cleaned data ──────────────────────────────────
df.to_csv('C:/Portfolio/car_prices_clean.csv', index=False)
df.to_excel('C:/Portfolio/car_prices_clean.xlsx', index=False)

print()
print("=== Done! ===")
print(f"Final rows: {len(df)}")
print(f"Final columns: {len(df.columns)}")
print()
print("=== Column Types ===")
print(df.dtypes)
print()
print("=== Numeric Summary ===")
print(df[['sellingprice', 'mmr', 'odometer',
          'car_age', 'price_vs_mmr_pct']].describe().round(2))
