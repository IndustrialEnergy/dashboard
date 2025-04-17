from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from layouts.base_layout import create_base_layout
from components.filters import create_filters
# Import charts
# from dashboard_app.charts import create_boxplot_cost_chart

def create_dashboard_page(integrated_df, boxplot_cost_df, boxplot_payback_df):
    content = html.Div([
        
        dbc.Row([
        dbc.Col(html.H1("Industrial Energy Efficiency Dashboard"), className="d-flex landing-page-title justify-content-center mb-4 mt-2")
        ]),
        
        # Left sidebar for filters
        dbc.Row([
        create_filters(boxplot_cost_df),
        ]),

        # Main content area for charts
        dbc.Col([

            # Active filters display
            html.Div([
                html.H6("Active Filters:", className="d-inline-block me-2"),
                html.Div(id="active-filters-display", className="d-inline-block")
            ], id="active-filters-container", className="mb-3 p-2 border-bottom"),

            # SECTION: Energy Metrics
            dbc.Row([
                dbc.Col(html.H4("Energy Metrics", className="section-header mb-3"), width=12)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Electricity Savings Distribution"),
                        dbc.CardBody([
                            html.Div(dcc.Graph(id="electricity-boxplot"), className="chart-container")
                        ])
                    ])
                ], width=6),

                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Other Fuels Savings Distribution"),
                        dbc.CardBody([
                            html.Div(dcc.Graph(id="other-fuels-boxplot"), className="chart-container")
                        ])
                    ])
                ], width=6),
            ]),

            # SECTION: Cost Metrics
            dbc.Row([
                dbc.Col(html.H4("Cost Metrics", className="section-header mt-4 mb-3"), width=12)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Implementation Cost Distribution (Adjusted to <current year>)"),
                        dbc.CardBody([
                            html.Div(dcc.Graph(id="cost-boxplot"), className="chart-container")
                        ])
                    ])
                ], width=6),

                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Payback Distribution"),
                        dbc.CardBody([
                            html.Div(dcc.Graph(id="payback-boxplot"), className="chart-container")
                        ])
                    ])
                ], width=6),
            ]),

            # SECTION: Emissions Metrics
            dbc.Row([
                dbc.Col(html.H4("Emissions Metrics", className="section-header mt-4 mb-3"), width=12)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Reduction in CO2"),
                        dbc.CardBody([
                            html.Div(dcc.Graph(id="co2-boxplot"), className="chart-container")
                        ])
                    ])
                ], width=4),

                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Reduction in SO2"),
                        dbc.CardBody([
                            html.Div(id="so2-boxplot", className="chart-container")
                        ])
                    ])
                ], width=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Reduction in NOx"),
                        dbc.CardBody([
                            html.Div(id="nox-boxplot", className="chart-container")
                        ])
                    ])
                ], width=4),
            ]),
            
        ], width=12),

        # SECTION: Table displaying an integrated dataset
        dbc.Row([
            dbc.Col(html.H4("Assessment Recommendations Table", className="section-header text-primary mt-4 mb-3"), width=12)
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Assessment Recommendations Table"),
                    dbc.CardBody([
                        html.Div(
                            dash_table.DataTable(
                                data=integrated_df.head(10).to_dict('records'), # demo: display only 10 records
                                columns=[{"name": i, "id": i} for i in integrated_df.columns],
                                style_table={'overflowX': 'scroll'},
                            ),
                            className="table-container"
                        )
                    ])
                ])
            ], width=12, className="mb-4"),
        ]),

    ], className="container-fluid p-4")
    
    return create_base_layout(content)
