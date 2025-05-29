from dash import Input, Output
from charts.boxplot_payback import create_boxplot_payback_chart
from components.filters import apply_wildcard_filter
import pandas as pd


def payback_boxplot_callback(app, boxplot_payback_df):
    @app.callback(
        Output("payback-boxplot", "figure"),
        Input("sector-filter", "value"),
        Input("fy-filter", "value"),
        Input("impstatus-filter", "value"),
        Input("arc-filter", "value"),
        Input("state-filter", "value"),
    )
    def update_outputs(naics_imputed, fy, impstatus, arc2, state):
        # print("\n=== Payback Boxplot Filtering Debug ===")
        # print(f"Initial dataframe shape: {boxplot_payback_df.shape}")
        # print(f"Initial data types:")
        # print(boxplot_payback_df.dtypes)
        # print("\nFilter values received:")
        # print(f"  NAICS codes: {naics_imputed}")
        # print(f"  Year range: {fy}")
        # print(f"  Implementation status: {impstatus}")
        # print(f"  ARC codes: {arc2}")
        # print(f"  States: {state}")

        # Start with full dataset
        dff = boxplot_payback_df.copy()
        # print(f"\nInitial dataset size: {len(dff)} rows")

        # Apply NAICS filter with wildcard support
        if naics_imputed:
            # print("\nNAICS filter debug:")
            # print(
            #     f"Unique NAICS in data: {dff['naics_imputed'].unique()}"
            # )
            # print(f"NAICS filter values: {naics_imputed}")
            dff = apply_wildcard_filter(dff, naics_imputed, "naics_imputed")
            # print(f"After NAICS filter: {len(dff)} rows")

        # Apply year range filter
        if fy and len(fy) == 2:
            # print("\nYear range filter debug:")
            # print(
            #     f"Year range in data: {dff['fy'].min()} to {dff['fy'].max()}"
            # )
            dff = dff[dff["fy"].between(fy[0], fy[1])]
            # print(f"After year range filter: {len(dff)} rows")

        # Apply implementation status filter
        if impstatus:
            # print("\nImplementation status filter debug:")
            # print(
            #     f"Unique statuses in data: {dff['impstatus'].unique()}"
            # )
            # print(f"Status filter values: {impstatus}")
            # print(f"Status column type: {dff['impstatus'].dtype}")
            # print(f"First few status values: {dff['impstatus'].head()}")
            dff = dff[dff["impstatus"].isin(impstatus)]
            # print(f"After implementation status filter: {len(dff)} rows")

        # Apply ARC filter with wildcard support
        if arc2:
            # print("\nARC filter debug:")
            # print(f"Unique ARCs in data: {dff['arc2'].unique()}")
            # print(f"ARC filter values: {arc2}")
            dff = apply_wildcard_filter(dff, arc2, "arc2")
            # print(f"After ARC filter: {len(dff)} rows")

        # Apply state filter
        if state:
            # print("\nState filter debug:")
            # print(f"Unique states in data: {dff['state'].unique()}")
            # print(f"State filter values: {state}")
            # print(f"State column type: {dff['state'].dtype}")
            # print(f"First few state values: {dff['state'].head()}")
            dff = dff[dff["state"].isin(state)]
            # print(f"After state filter: {len(dff)} rows")

        # print("\nFinal data summary:")
        # if not dff.empty:
        #     print(f"Final shape: {dff.shape}")
        #     print("\nSample of filtered data:")
        #     print(dff[["fy", "state", "arc2", "naics_imputed", "impstatus"]].head())
        # else:
        #     print("WARNING: No data after filtering!")

        return create_boxplot_payback_chart(dff)
