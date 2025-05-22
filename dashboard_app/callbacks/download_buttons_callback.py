from dash import dcc, Output, Input

def download_excel(app, get_data_function):
    @app.callback(
        Output("download-excel", "data"),
        Input("btn-download-excel", "n_clicks"),
        prevent_initial_call=True,
    )
    def download_excel_callback(n_clicks):
        if n_clicks > 0:
            df = get_data_function()
            return dcc.send_data_frame(df.to_excel, "IAC_Database.xlsx", sheet_name="Sheet1")
    return download_excel_callback

def download_csv(app):
    @app.callback(
        Output("download-csv", "data"),
        Input("btn-download-csv", "n_clicks"),
        prevent_initial_call=True,
    )
    def download_csv_callback(n_clicks):
        if n_clicks > 0:
            from dashboard_app.components.download_buttons import get_data_from_zip
            df = get_data_from_zip()
            return dcc.send_data_frame(df.to_csv, "IAC_Database.csv", index=False)
    return download_csv_callback