from dash import Input, Output
from charts.boxplot_nox import create_boxplot_nox_chart
from components.filter_outliers import filter_outliers
import pandas as pd


def emissions_nox_callback(app, boxplot_nox_df):
    @app.callback(
        Output("nox-boxplot", "figure"),
        Input("sector-filter", "value"),
        Input("fy-filter", "value"),
        Input("impstatus-filter", "value"),
        Input("arc-filter", "value"),
        Input("state-filter", "value"),
        Input("outlier-filter", "value")
    )
    def update_outputs(naics_imputed, fy_range, impstatus, arc2, state, remove_outliers):
        # create a mask for each filter
        mask = pd.Series(True, index=boxplot_nox_df.index)
        dummy_df = boxplot_nox_df[(boxplot_nox_df['state'] == 'TX') & (boxplot_nox_df['arc2'] == '2.7492')]
    
        if naics_imputed:
            mask &= boxplot_nox_df["naics_imputed"].isin(naics_imputed)
        if fy_range:  # Handling range slider correctly
            min_year, max_year = fy_range  # Unpack the range values
            mask &= (boxplot_nox_df["fy"] >= min_year) & (boxplot_nox_df["fy"] <= max_year)
        if impstatus:
            mask &= boxplot_nox_df["impstatus"].isin(impstatus)
        if arc2:
            mask &= boxplot_nox_df["arc2"].isin(arc2)
        if state:
            mask &= boxplot_nox_df["state"].isin(state)

        # apply all filters at once
        dff = boxplot_nox_df[mask]

        if remove_outliers:
            dff = filter_outliers(dff,"emissions_avoided", std_threshold=2)

        # [TEST - REMOVE BEFORE PROD] print filtered data info
        print(f"dummy: {dummy_df.head(30)}")
        print(f"dummy: {dummy_df.shape}")
        # print(f"Filtered unique statuses: {dff['impstatus'].unique()}")
        print(f"Filtered data shape: {dff.shape}")
        print(dff.head(30))
        

        return create_boxplot_nox_chart(dff)