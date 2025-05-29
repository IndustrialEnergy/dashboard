import pandas as pd

# Load data directly
df = pd.read_csv("data/final/iac_integrated.csv")

print("=== IMPLEMENTATION STATUS ANALYSIS ===")
print()

print("1. Full dataset implementation status distribution:")
full_dist = df["impstatus"].value_counts()
print(full_dist)
print(f"Total records: {len(df)}")
print()


# Apply wildcard filter manually
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


# Apply typical default filters
print("2. After state filter (CA, TX, CO):")
filtered_df = df[df["state"].isin(["CA", "TX", "CO"])]
state_dist = filtered_df["impstatus"].value_counts()
print(state_dist)
print(f"Total records: {len(filtered_df)}")
print()

print("3. After NAICS filter (332812, 332813, 334418):")
filtered_df = filtered_df[
    filtered_df["naics_imputed"].isin(["332812", "332813", "334418"])
]
naics_dist = filtered_df["impstatus"].value_counts()
print(naics_dist)
print(f"Total records: {len(filtered_df)}")
print()

print("4. After ARC filter (2.41*, 2.4133):")
filtered_df = apply_wildcard_filter_simple(filtered_df, ["2.41*", "2.4133"], "arc2")
arc_dist = filtered_df["impstatus"].value_counts()
print(arc_dist)
print(f"Total records: {len(filtered_df)}")
if len(filtered_df) > 0:
    print("Sample ARC codes in filtered data:")
    print(sorted(filtered_df["arc2"].unique())[:10])
print()

print("=== MOTOR SYSTEMS ANALYSIS ===")
print()

# Look specifically at motor systems
motor_df = apply_wildcard_filter_simple(df, ["2.4*"], "arc2")
print("Motor Systems (2.4*) implementation distribution in full dataset:")
motor_dist = motor_df["impstatus"].value_counts()
print(motor_dist)
print(f"Motor systems records: {len(motor_df)}")
print()

# Compare with other categories
thermal_df = apply_wildcard_filter_simple(df, ["2.2*"], "arc2")
print("Thermal Systems (2.2*) implementation distribution:")
thermal_dist = thermal_df["impstatus"].value_counts()
print(thermal_dist)
print(f"Thermal systems records: {len(thermal_df)}")
print()

electrical_df = apply_wildcard_filter_simple(df, ["2.3*"], "arc2")
print("Electrical Power (2.3*) implementation distribution:")
electrical_dist = electrical_df["impstatus"].value_counts()
print(electrical_dist)
print(f"Electrical systems records: {len(electrical_df)}")
print()

print("=== IMPLEMENTATION RATE COMPARISON ===")


def calc_impl_rate(dist):
    if "I" not in dist.index or "N" not in dist.index:
        return "N/A"
    return f"{dist['I'] / (dist['I'] + dist['N']) * 100:.1f}%"


print(f"Motor Systems implementation rate: {calc_impl_rate(motor_dist)}")
print(f"Thermal Systems implementation rate: {calc_impl_rate(thermal_dist)}")
print(f"Electrical Systems implementation rate: {calc_impl_rate(electrical_dist)}")
if len(arc_dist) > 0:
    print(f"Your filtered data implementation rate: {calc_impl_rate(arc_dist)}")

print()
print("=== SPECIFIC 2.41 ANALYSIS ===")
motor_241 = apply_wildcard_filter_simple(df, ["2.41*"], "arc2")
print("Motor equipment (2.41*) implementation distribution:")
motor_241_dist = motor_241["impstatus"].value_counts()
print(motor_241_dist)
print(f"Implementation rate: {calc_impl_rate(motor_241_dist)}")
