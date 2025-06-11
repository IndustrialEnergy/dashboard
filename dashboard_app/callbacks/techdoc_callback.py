import os
from components.techdoc_downloadbttn import get_td_from_local
from dash import dcc, Output, Input

def download_td_pdf(app, get_file_function=None):
    if get_file_function is None:
        get_file_function = get_td_from_local
    
    @app.callback(
        Output("download-td-pdf", "data"),  # Changed to unique ID
        Input("btn-td-download-pdf", "n_clicks"),
        prevent_initial_call=True,
    )
    def download_td_pdf_callback(n_clicks):
        if n_clicks and n_clicks > 0:
            file_path = get_file_function()
            if file_path and os.path.exists(file_path):
                return dcc.send_file(file_path, filename="IndustrialEnergy_TechnicalDocumentation.pdf")
        return None
    
    return download_td_pdf_callback