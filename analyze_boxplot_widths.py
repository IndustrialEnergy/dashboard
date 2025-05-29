import pandas as pd
import numpy as np

# Load data directly
df = pd.read_csv("data/final/iac_integrated.csv")


def apply_wildcard_filter_simple(df, filter_values, column_name):
    if not filter_values:
        return df

    mask = pd.Series(False, index=df.index)

    for value in filter_values:
        if str(value).endswith("*"):
            pattern = str(value)[:-1]  # Remove the *
            mask |= df[column_name].astype(str).str.startswith(pattern)
        else:
            mask |= df[column_name] == value

    return df[mask]


def filter_outliers(df, column_name, std_threshold=2):
    if df.empty or column_name not in df.columns:
        return df
    mean = df[column_name].mean()
    std = df[column_name].std()
    return df[
        (df[column_name] >= mean - std_threshold * std)
        & (df[column_name] <= mean + std_threshold * std)
    ]


# Apply the same filters as in the dashboard
print("=== BOX PLOT WIDTH ANALYSIS ===")
print()

# Simulate your current filters
states = ["CA", "TX", "CO"]
naics_codes = ["332812", "332813", "334418"]
arc_codes = ["2.41*", "2.4133"]
impl_status = ["I", "N"]  # Implemented and Not Implemented

# Apply filters step by step
filtered_df = df[df["state"].isin(states)]
filtered_df = filtered_df[filtered_df["naics_imputed"].isin(naics_codes)]
filtered_df = apply_wildcard_filter_simple(filtered_df, arc_codes, "arc2")
filtered_df = filtered_df[filtered_df["impstatus"].isin(impl_status)]

print(f"Total filtered records: {len(filtered_df)}")
print()

# Analyze Implementation Cost
print("=== IMPLEMENTATION COST ANALYSIS ===")
cost_data = filtered_df["impcost_adj"].dropna()
print(f"Records with cost data: {len(cost_data)}")
print(f"Missing cost data: {len(filtered_df) - len(cost_data)}")

if len(cost_data) > 0:
    print(f"Cost statistics:")
    print(f"  Mean: ${cost_data.mean():,.2f}")
    print(f"  Median: ${cost_data.median():,.2f}")
    print(f"  Std Dev: ${cost_data.std():,.2f}")
    print(f"  Min: ${cost_data.min():,.2f}")
    print(f"  Max: ${cost_data.max():,.2f}")
    print(f"  IQR: ${cost_data.quantile(0.75) - cost_data.quantile(0.25):,.2f}")

    # Apply outlier filtering
    cost_filtered = filter_outliers(filtered_df, "impcost_adj", 2)[
        "impcost_adj"
    ].dropna()
    print(f"After outlier filtering (2σ): {len(cost_filtered)} records")
    print(f"Outliers removed: {len(cost_data) - len(cost_filtered)}")

    # Check by implementation status
    cost_impl = filtered_df[filtered_df["impstatus"] == "I"]["impcost_adj"].dropna()
    cost_not_impl = filtered_df[filtered_df["impstatus"] == "N"]["impcost_adj"].dropna()
    print(f"Implemented records with cost: {len(cost_impl)}")
    print(f"Not implemented records with cost: {len(cost_not_impl)}")

print()

# Analyze Payback Period
print("=== PAYBACK PERIOD ANALYSIS ===")
payback_data = filtered_df["payback_imputed"].dropna()
print(f"Records with payback data: {len(payback_data)}")
print(f"Missing payback data: {len(filtered_df) - len(payback_data)}")

if len(payback_data) > 0:
    print(f"Payback statistics:")
    print(f"  Mean: {payback_data.mean():.2f} years")
    print(f"  Median: {payback_data.median():.2f} years")
    print(f"  Std Dev: {payback_data.std():.2f} years")
    print(f"  Min: {payback_data.min():.2f} years")
    print(f"  Max: {payback_data.max():.2f} years")
    print(
        f"  IQR: {payback_data.quantile(0.75) - payback_data.quantile(0.25):.2f} years"
    )

    # Apply outlier filtering
    payback_filtered = filter_outliers(filtered_df, "payback_imputed", 2)[
        "payback_imputed"
    ].dropna()
    print(f"After outlier filtering (2σ): {len(payback_filtered)} records")
    print(f"Outliers removed: {len(payback_data) - len(payback_filtered)}")

    # Check by implementation status
    payback_impl = filtered_df[filtered_df["impstatus"] == "I"][
        "payback_imputed"
    ].dropna()
    payback_not_impl = filtered_df[filtered_df["impstatus"] == "N"][
        "payback_imputed"
    ].dropna()
    print(f"Implemented records with payback: {len(payback_impl)}")
    print(f"Not implemented records with payback: {len(payback_not_impl)}")

print()

# Data availability comparison
print("=== DATA AVAILABILITY COMPARISON ===")
both_metrics = filtered_df[["impcost_adj", "payback_imputed"]].dropna()
print(f"Records with BOTH cost and payback data: {len(both_metrics)}")

only_cost = filtered_df[
    filtered_df["impcost_adj"].notna() & filtered_df["payback_imputed"].isna()
]
only_payback = filtered_df[
    filtered_df["payback_imputed"].notna() & filtered_df["impcost_adj"].isna()
]
print(f"Records with ONLY cost data: {len(only_cost)}")
print(f"Records with ONLY payback data: {len(only_payback)}")

print()
print("=== COEFFICIENT OF VARIATION (relative spread) ===")
if len(cost_data) > 0:
    cost_cv = cost_data.std() / cost_data.mean() * 100
    print(f"Implementation Cost CV: {cost_cv:.1f}%")

if len(payback_data) > 0:
    payback_cv = payback_data.std() / payback_data.mean() * 100
    print(f"Payback Period CV: {payback_cv:.1f}%")

print("\nNote: Higher CV indicates wider relative spread in the data.")
