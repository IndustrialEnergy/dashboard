from dash import Input, Output
from charts.boxplot_natural_gas import create_boxplot_natural_gas_chart
from components.filter_outliers import filter_outliers
import pandas as pd


def natural_gas_callback(app, boxplot_natural_gas_df):
    @app.callback(
        Output("natural-gas-boxplot", "figure"),
        Input("sector-filter", "value"),
        Input("fy-filter", "value"),
        Input("impstatus-filter", "value"),
        Input("arc-filter", "value"),
        Input("state-filter", "value"),
        Input("outlier-filter", "value")
    )
    def update_outputs(naics_imputed, fy_range, impstatus, arc2, state, remove_outliers):
        # create a mask for each filter
        mask = pd.Series(True, index=boxplot_natural_gas_df.index)
    
        if naics_imputed:
            mask &= boxplot_natural_gas_df["naics_imputed"].isin(naics_imputed)
        if fy_range:  # Handling range slider correctly
            min_year, max_year = fy_range  # Unpack the range values
            mask &= (boxplot_natural_gas_df["fy"] >= min_year) & (boxplot_natural_gas_df["fy"] <= max_year)
        if impstatus:
            mask &= boxplot_natural_gas_df["impstatus"].isin(impstatus)
        if arc2:
            mask &= boxplot_natural_gas_df["arc2"].isin(arc2)
        if state:
            mask &= boxplot_natural_gas_df["state"].isin(state)

        # apply all filters at once
        dff = boxplot_natural_gas_df[mask]

        if remove_outliers:
            dff = filter_outliers(dff,"conserved", std_threshold=2)
        

        return create_boxplot_natural_gas_chart(dff)