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
    def update_outputs(naics_imputed, fy_range, impstatus, arc2, state, remove_outliers):
        # create a mask for each filter
        mask = pd.Series(True, index=boxplot_cost_df.index)
        dummy_df = boxplot_cost_df[
            (boxplot_cost_df["state"] == "TX") & (boxplot_cost_df["arc2"] == "2.7492")
        ]

        if naics_imputed:
            mask &= boxplot_cost_df["naics_imputed"].isin(naics_imputed)
        if fy_range:  # Handling range slider correctly
            min_year, max_year = fy_range  # Unpack the range values
            mask &= (boxplot_cost_df["fy"] >= min_year) & (
                boxplot_cost_df["fy"] <= max_year
            )
        if impstatus:
            mask &= boxplot_cost_df["impstatus"].isin(impstatus)
        if arc2:
            mask &= boxplot_cost_df["arc2"].isin(arc2)
        if state:
            mask &= boxplot_cost_df["state"].isin(state)

        # apply all filters at once
        dff = boxplot_cost_df[mask]

        if remove_outliers:
            dff = filter_outliers(dff, "impcost_adj", std_threshold=2)

        # [TEST - REMOVE BEFORE PROD] print filtered data info
        print(f"dummy: {dummy_df.head(30)}")
        print(f"dummy: {dummy_df.shape}")
        # print(f"Filtered unique statuses: {dff['impstatus'].unique()}")
        print(f"Filtered data shape: {dff.shape}")
        print(dff.head(30))

        return create_boxplot_cost_chart(dff)
