from dash import Input, Output
from charts.boxplot_cost import create_boxplot_cost_chart
from components.filter_outliers import filter_outliers
from components.filters import apply_wildcard_filter
import pandas as pd


def cost_boxplot_callback(app, boxplot_cost_df):
    @app.callback(
        Output("cost-boxplot", "figure"),
        Input("sector-filter", "value"),
        Input("fy-filter", "value"),
        Input("impstatus-filter", "value"),
        Input("arc-filter", "value"),
        Input("state-filter", "value"),
        Input("outlier-filter", "value"),
    )
    def update_outputs(
        naics_imputed, fy_range, impstatus, arc2, state, remove_outliers
    ):
        # print("\n=== Cost Boxplot Filtering Debug ===")
        # print(f"Initial dataframe shape: {boxplot_cost_df.shape}")
        # print(f"Initial data types:")
        # print(boxplot_cost_df.dtypes)
        # print("\nFilter values received:")
        # print(f"  NAICS codes: {naics_imputed}")
        # print(f"  Year range: {fy_range}")
        # print(f"  Implementation status: {impstatus}")
        # print(f"  ARC codes: {arc2}")
        # print(f"  States: {state}")
        # print(f"  Remove outliers: {remove_outliers}")

        # Start with full dataset
        dff = boxplot_cost_df.copy()
        print(f"\nInitial dataset size: {len(dff)} rows")

        # Apply NAICS filter with wildcard support
        if naics_imputed:
            print("\nNAICS filter debug:")
            print(f"Unique NAICS in data: {dff['naics_imputed'].unique()}")
            print(f"NAICS filter values: {naics_imputed}")
            dff = apply_wildcard_filter(dff, naics_imputed, "naics_imputed")
            print(f"After NAICS filter: {len(dff)} rows")

        # Apply year range filter
        if fy_range:  # Handling range slider correctly
            print("\nYear range filter debug:")
            print(f"Year range in data: {dff['fy'].min()} to {dff['fy'].max()}")
            min_year, max_year = fy_range  # Unpack the range values
            dff = dff[(dff["fy"] >= min_year) & (dff["fy"] <= max_year)]
            print(f"After year range filter: {len(dff)} rows")

        # Apply implementation status filter
        if impstatus:
            print("\nImplementation status filter debug:")
            print(f"Unique statuses in data: {dff['impstatus'].unique()}")
            print(f"Status filter values: {impstatus}")
            print(f"Status column type: {dff['impstatus'].dtype}")
            print(f"First few status values: {dff['impstatus'].head()}")
            dff = dff[dff["impstatus"].isin(impstatus)]
            print(f"After implementation status filter: {len(dff)} rows")

        # Apply ARC filter with wildcard support
        if arc2:
            print("\nARC filter debug:")
            print(f"Unique ARCs in data: {dff['arc2'].unique()}")
            print(f"ARC filter values: {arc2}")
            dff = apply_wildcard_filter(dff, arc2, "arc2")
            print(f"After ARC filter: {len(dff)} rows")

        # Apply state filter
        if state:
            print("\nState filter debug:")
            print(f"Unique states in data: {dff['state'].unique()}")
            print(f"State filter values: {state}")
            print(f"State column type: {dff['state'].dtype}")
            print(f"First few state values: {dff['state'].head()}")
            dff = dff[dff["state"].isin(state)]
            print(f"After state filter: {len(dff)} rows")

        # Apply outlier removal
        if remove_outliers:
            print("\nOutlier removal debug:")
            print(f"Before outlier removal: {len(dff)} rows")
            dff = filter_outliers(dff, "impcost_adj", std_threshold=2)
            print(f"After outlier removal: {len(dff)} rows")

        print("\nFinal data summary:")
        if not dff.empty:
            print(f"Final shape: {dff.shape}")
            print("\nSample of filtered data:")
            print(dff[["fy", "state", "arc2", "naics_imputed", "impstatus"]].head())
        else:
            print("WARNING: No data after filtering!")

        return create_boxplot_cost_chart(dff)
