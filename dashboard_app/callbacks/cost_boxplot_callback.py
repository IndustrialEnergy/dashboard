from dash import Input, Output
from charts.boxplot_cost import create_boxplot_cost_chart
import pandas as pd


def cost_boxplot_callback(app, boxplot_cost_df):
    @app.callback(
        Output("cost-boxplot", "figure"),
        Input("sector-filter", "value"),
        Input("fy-filter", "value"),
        Input("impstatus-filter", "value"),
        Input("arc-filter", "value"),
        Input("state-filter", "value"),
    )
    def update_outputs(sector, fy, impstatus, arc2, state):
        # create a mask for each filter
        mask = pd.Series(True, index=boxplot_cost_df.index)

        if sector:
            mask &= boxplot_cost_df["sector"].isin(sector)
        if fy:
            mask &= boxplot_cost_df["fy"].isin(fy)
        if impstatus:
            mask &= boxplot_cost_df["impstatus"].isin(impstatus)
        if arc2:
            mask &= boxplot_cost_df["arc2"].isin(arc2)
        if state:
            mask &= boxplot_cost_df["state"].isin(state)

        # apply all filters at once
        dff = boxplot_cost_df[mask]

        # [TEST - REMOVE BEFORE PROD] print filtered data info
        print(f"Filtered unique statuses: {dff['impstatus'].unique()}")
        print(f"Filtered data shape: {dff.shape}")

        return create_boxplot_cost_chart(dff)
