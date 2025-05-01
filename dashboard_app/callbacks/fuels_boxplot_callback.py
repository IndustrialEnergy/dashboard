from dash import Input, Output
from charts.boxplot_fuels import create_boxplot_fuels_chart
from components.filter_outliers import filter_outliers
import pandas as pd


def emissions_fuels_callback(app, boxplot_fuels_df):
    @app.callback(
        Output("other-fuels-boxplot", "figure"),
        Input("sector-filter", "value"),
        Input("fy-filter", "value"),
        Input("impstatus-filter", "value"),
        Input("arc-filter", "value"),
        Input("state-filter", "value"),
        Input("outlier-filter", "value")
    )
    def update_outputs(sector, fy_range, impstatus, arc2, state, remove_outliers):
        # create a mask for each filter
        mask = pd.Series(True, index=boxplot_fuels_df.index)
        dummy_df = boxplot_fuels_df[(boxplot_fuels_df['state'] == 'TX') & (boxplot_fuels_df['arc2'] == '2.7492')]
    
        if sector:
            mask &= boxplot_fuels_df["sector"].isin(sector)
        if fy_range:  # Handling range slider correctly
            min_year, max_year = fy_range  # Unpack the range values
            mask &= (boxplot_fuels_df["fy"] >= min_year) & (boxplot_fuels_df["fy"] <= max_year)
        if impstatus:
            mask &= boxplot_fuels_df["impstatus"].isin(impstatus)
        if arc2:
            mask &= boxplot_fuels_df["arc2"].isin(arc2)
        if state:
            mask &= boxplot_fuels_df["state"].isin(state)

        # apply all filters at once
        dff = boxplot_fuels_df[mask]

        if remove_outliers:
            dff = filter_outliers(dff,"emissions_avoided", std_threshold=2)

        # [TEST - REMOVE BEFORE PROD] print filtered data info
        print(f"dummy: {dummy_df.head(30)}")
        print(f"dummy: {dummy_df.shape}")
        # print(f"Filtered unique statuses: {dff['impstatus'].unique()}")
        print(f"Filtered data shape: {dff.shape}")
        print(dff.head(30))
        

        return create_boxplot_fuels_chart(dff)