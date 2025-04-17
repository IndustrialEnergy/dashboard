from dash import Input, Output
from charts.boxplot_cost import create_boxplot_cost_chart

def cost_boxplot_callback(app, boxplot_cost_df, integrated_df,  boxplot_payback_df):
    @app.callback(
        Output("cost-boxplot", "figure"),
        #Output("recommendation-table", "children"),
        Input("naics-filter", "value"),
        Input("fy-filter", "value"),
        Input("impstatus-filter", "value"),
        Input("arc2-filter", "value"),
    )
    def update_outputs(naics, fy, impstatus, arc2):
        dff = boxplot_cost_df.copy()

        if naics:
            dff = dff[dff["naics"].isin(naics)]
        if fy:
            dff = dff[dff["fy"].isin(fy)]
        if impstatus:
            dff = dff[dff["impstatus"].isin(impstatus)]
        if arc2:
            dff = dff[dff["arc2"].isin(arc2)]

        return create_boxplot_cost_chart(dff)
