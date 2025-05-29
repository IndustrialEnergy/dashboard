from dash import Input, Output
from charts.boxplot_cost import create_boxplot_cost_chart
from components.filter_outliers import filter_outliers
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

        # create a mask for each filter
        mask = pd.Series(True, index=boxplot_cost_df.index)
        print(f"\nInitial mask size: {mask.sum()} rows")

        if naics_imputed:
            print("\nNAICS filter debug:")
            print(f"Unique NAICS in data: {boxplot_cost_df['naics_imputed'].unique()}")
            print(f"NAICS filter values: {naics_imputed}")
            mask &= boxplot_cost_df["naics_imputed"].isin(naics_imputed)
            print(f"After NAICS filter: {mask.sum()} rows")

        if fy_range:  # Handling range slider correctly
            print("\nYear range filter debug:")
            print(
                f"Year range in data: {boxplot_cost_df['fy'].min()} to {boxplot_cost_df['fy'].max()}"
            )
            min_year, max_year = fy_range  # Unpack the range values
            mask &= (boxplot_cost_df["fy"] >= min_year) & (
                boxplot_cost_df["fy"] <= max_year
            )
            print(f"After year range filter: {mask.sum()} rows")

        if impstatus:
            print("\nImplementation status filter debug:")
            print(f"Unique statuses in data: {boxplot_cost_df['impstatus'].unique()}")
            print(f"Status filter values: {impstatus}")
            print(f"Status column type: {boxplot_cost_df['impstatus'].dtype}")
            print(f"First few status values: {boxplot_cost_df['impstatus'].head()}")
            mask &= boxplot_cost_df["impstatus"].isin(impstatus)
            print(f"After implementation status filter: {mask.sum()} rows")

        if arc2:
            print("\nARC filter debug:")
            print(f"Unique ARCs in data: {boxplot_cost_df['arc2'].unique()}")
            print(f"ARC filter values: {arc2}")
            mask &= boxplot_cost_df["arc2"].isin(arc2)
            print(f"After ARC filter: {mask.sum()} rows")

        if state:
            print("\nState filter debug:")
            print(f"Unique states in data: {boxplot_cost_df['state'].unique()}")
            print(f"State filter values: {state}")
            print(f"State column type: {boxplot_cost_df['state'].dtype}")
            print(f"First few state values: {boxplot_cost_df['state'].head()}")
            mask &= boxplot_cost_df["state"].isin(state)
            print(f"After state filter: {mask.sum()} rows")

        # apply all filters at once
        dff = boxplot_cost_df[mask]

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
