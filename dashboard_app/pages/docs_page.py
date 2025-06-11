from dash import html, dcc
import dash_bootstrap_components as dbc
from layouts.base_layout import create_base_layout

def create_docs_page():
    content = html.Div([
        # Header Section
        dbc.Row([
            dbc.Col([
                html.H3("Documentation", 
                       className="d-flex landing-page-title justify-content-center mb-4 mt-4"),
            ])
        ]),
        
        # User Guide Card Section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("User Guide", 
                               className="mb-0", 
                               style={"color": "#003660", "fontWeight": "bold"})
                    ]),
                    dbc.CardBody([
                        html.P([
                            "Download the comprehensive user guide to learn how to navigate and use all features of the Industrial Energy Dashboard. ",
                            "This guide includes step-by-step instructions, feature explanations, and best practices for data exploration."
                        ], className="card-text mb-3"),
                        
                        html.Div([
                            dbc.Button([
                                html.I(className="fas fa-download me-2"),
                                "Download User Guide (PDF)"
                            ],
                            id="btn-ug-download-pdf",
                            color="primary",
                            size="lg",
                            className="d-flex align-items-center justify-content-center")
                        ], className="d-grid"),
                        
                        # Download component
                        dcc.Download(id="download-pdf")
                    ])
                ], className="mb-4 border-start border-primary border-3 shadow-sm")
            ], md=8, lg=6, className="mx-auto")
        ]),
        # Tech Doc Card Section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Technical Documentation", 
                               className="mb-0", 
                               style={"color": "#003660", "fontWeight": "bold"})
                    ]),
                    dbc.CardBody([
                        html.P([
                            "Download the comprehensive technical documentation on the creation and implementation processes of our Capstone project - from integrating the dataset to creating the dashboard."
                        ], className="card-text mb-3"),
                        
                        html.Div([
                            dbc.Button([
                                html.I(className="fas fa-download me-2"),
                                "Download User Guide (PDF)"
                            ],
                            id="btn-td-download-pdf",
                            color="primary",
                            size="lg",
                            className="d-flex align-items-center justify-content-center")
                        ], className="d-grid"),
                        
                        # Download component
                        dcc.Download(id="download-pdf")
                    ])
                ], className="mb-4 border-start border-primary border-3 shadow-sm")
            ], md=8, lg=6, className="mx-auto")
        ]),
    ])
    
    return create_base_layout(content)