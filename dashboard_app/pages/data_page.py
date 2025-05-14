from dash import html, dcc
import dash_bootstrap_components as dbc
from layouts.base_layout import create_base_layout
import pandas as pd

def create_data_page():
    content = html.Div(
        [
            dbc.Row( # Create header
                [
                    dbc.Col(
                        html.H3("Download the Data"),
                        className="d-flex landing-page-title justify-content-center mb-4 mt-3",
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    html.H6("Download Data:", className="d-inline-block me-2"),
                                    dbc.Button(
                                        [html.I(className="fas fa-file-excel me-2"), "Excel"],
                                        id="btn-download-excel", 
                                        color="success", 
                                        className="me-2"
                                    ),
                                    dbc.Button(
                                        [html.I(className="fas fa-file-csv me-2"), "CSV"], 
                                        id="btn-download-csv", 
                                        color="primary", 
                                        className="me-2"
                                    ),
                                    dbc.Tooltip(
                                        "Download data as Excel file",
                                        target="btn-download-excel"
                                    ),
                                    dbc.Tooltip(
                                        "Download data as CSV file",
                                        target="btn-download-csv"
                                    ),
                                    # Essential components for dowload function
                                    dcc.Download(id="download-excel"),
                                    dcc.Download(id="download-csv"),
                                ],
                                className="d-flex align-items-center justify-content-end mb-3",
                            )
                        ],
                        width=12,
                    )
                ]
            )
        ]
    )
    return create_base_layout(content)


