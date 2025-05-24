from dash import Input, Output
from charts.boxplot_payback import create_boxplot_payback_chart
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
        print("\n=== Payback Boxplot Filtering Debug ===")
        print(f"Initial dataframe shape: {boxplot_payback_df.shape}")
        print(f"Initial data types:")
        print(boxplot_payback_df.dtypes)
        print("\nFilter values received:")
        print(f"  NAICS codes: {naics_imputed}")
        print(f"  Year range: {fy}")
        print(f"  Implementation status: {impstatus}")
        print(f"  ARC codes: {arc2}")
        print(f"  States: {state}")

        # create a mask for each filter
        mask = pd.Series(True, index=boxplot_payback_df.index)
        print(f"\nInitial mask size: {mask.sum()} rows")

        if naics_imputed:
            print("\nNAICS filter debug:")
            print(
                f"Unique NAICS in data: {boxplot_payback_df['naics_imputed'].unique()}"
            )
            print(f"NAICS filter values: {naics_imputed}")
            mask &= boxplot_payback_df["naics_imputed"].isin(naics_imputed)
            print(f"After NAICS filter: {mask.sum()} rows")

        if fy and len(fy) == 2:
            print("\nYear range filter debug:")
            print(
                f"Year range in data: {boxplot_payback_df['fy'].min()} to {boxplot_payback_df['fy'].max()}"
            )
            mask &= boxplot_payback_df["fy"].between(fy[0], fy[1])
            print(f"After year range filter: {mask.sum()} rows")

        if impstatus:
            print("\nImplementation status filter debug:")
            print(
                f"Unique statuses in data: {boxplot_payback_df['impstatus'].unique()}"
            )
            print(f"Status filter values: {impstatus}")
            print(f"Status column type: {boxplot_payback_df['impstatus'].dtype}")
            print(f"First few status values: {boxplot_payback_df['impstatus'].head()}")
            mask &= boxplot_payback_df["impstatus"].isin(impstatus)
            print(f"After implementation status filter: {mask.sum()} rows")

        if arc2:
            print("\nARC filter debug:")
            print(f"Unique ARCs in data: {boxplot_payback_df['arc2'].unique()}")
            print(f"ARC filter values: {arc2}")
            mask &= boxplot_payback_df["arc2"].isin(arc2)
            print(f"After ARC filter: {mask.sum()} rows")

        if state:
            print("\nState filter debug:")
            print(f"Unique states in data: {boxplot_payback_df['state'].unique()}")
            print(f"State filter values: {state}")
            print(f"State column type: {boxplot_payback_df['state'].dtype}")
            print(f"First few state values: {boxplot_payback_df['state'].head()}")
            mask &= boxplot_payback_df["state"].isin(state)
            print(f"After state filter: {mask.sum()} rows")

        # apply all filters at once
        dff = boxplot_payback_df[mask]

        print("\nFinal data summary:")
        if not dff.empty:
            print(f"Final shape: {dff.shape}")
            print("\nSample of filtered data:")
            print(dff[["fy", "state", "arc2", "naics_imputed", "impstatus"]].head())
        else:
            print("WARNING: No data after filtering!")

        return create_boxplot_payback_chart(dff)
