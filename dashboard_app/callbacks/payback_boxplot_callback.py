from dash import Input, Output
from charts.boxplot_payback import create_boxplot_payback_chart
from helpers.filter_outliers import filter_outliers
from helpers.apply_wildcard_filter import apply_wildcard_filter
import pandas as pd


def payback_boxplot_callback(app, boxplot_payback_df):
    @app.callback(
        Output("payback-boxplot", "figure"),
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
        # Start with full dataset
        dff = boxplot_payback_df.copy()

        # Apply NAICS filter with wildcard support
        if naics_imputed:
            dff = apply_wildcard_filter(dff, naics_imputed, "naics_imputed")

        # Apply year range filter
        if fy_range:  # Handling range slider correctly
            min_year, max_year = fy_range  # Unpack the range values
            dff = dff[(dff["fy"] >= min_year) & (dff["fy"] <= max_year)]

        # Apply implementation status filter
        if impstatus:
            dff = dff[dff["impstatus"].isin(impstatus)]

        # Apply ARC filter with wildcard support
        if arc2:
            dff = apply_wildcard_filter(dff, arc2, "arc2")

        # Apply state filter
        if state:
            dff = dff[dff["state"].isin(state)]

        # Apply outlier removal
        if remove_outliers:
            dff = filter_outliers(dff, "payback_imputed", std_threshold=remove_outliers)

        return create_boxplot_payback_chart(dff)
