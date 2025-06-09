from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from layouts.base_layout import create_base_layout
from components.filters import create_filters
import json
from pathlib import Path
# Import charts
# from dashboard_app.charts import create_boxplot_cost_chart


def create_dashboard_page(filters_df, reference_year):
    # Read metadata for last updated
    try:
        metadata_path = Path("data/final/iac_metadata.json")
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
        last_updated = metadata["data_info"]["last_updated"]
    except:
        last_updated = "Unknown"

    content = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.H1("Industrial Energy Efficiency Dashboard"),
                        className="d-flex landing-page-title justify-content-center mb-4 mt-2",
                    )
                ]
            ),
            # Filters row
            dbc.Row(
                [
                    create_filters(filters_df),
                ]
            ),
            # # Last updated row
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    f"Based on IAC assessment data from: {last_updated} | ",
                                    html.A("View all data sources", href="/data"),
                                ],
                                className="info-section",
                            )
                        ],
                        width=12,
                    )
                ]
            ),
            # Main content area for charts
            dbc.Col(
                [
                    # # Active filters display
                    # html.Div(
                    #     [
                    #         html.H6("Active Filters:", className="d-inline-block me-2"),
                    #         html.Div(
                    #             id="active-filters-display", className="d-inline-block"
                    #         ),
                    #     ],
                    #     id="active-filters-container",
                    #     className="mb-3 p-2 border-bottom",
                    # ),
                    # SECTION: Energy Metrics
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H4(
                                    "Energy Metrics", className="section-header mb-3"
                                ),
                                width=12,
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dbc.Card(
                                        [
                                            dbc.CardHeader(
                                                "Annual Electricity Savings Distribution"
                                            ),
                                            dbc.CardBody(
                                                [
                                                    html.Div(
                                                        dcc.Graph(
                                                            id="electricity-boxplot"
                                                        ),
                                                        className="chart-container boxplot-chart",
                                                    )
                                                ]
                                            ),
                                        ]
                                    )
                                ],
                                width=4,
                            ),
                            dbc.Col(
                                [
                                    dbc.Card(
                                        [
                                            dbc.CardHeader(
                                                "Annual Natural Gas Savings Distribution"
                                            ),
                                            dbc.CardBody(
                                                [
                                                    html.Div(
                                                        dcc.Graph(
                                                            id="natural-gas-boxplot"
                                                        ),
                                                        className="chart-container boxplot-chart",
                                                    )
                                                ]
                                            ),
                                        ]
                                    )
                                ],
                                width=4,
                            ),
                            dbc.Col(
                                [
                                    dbc.Card(
                                        [
                                            dbc.CardHeader(
                                                "Annual Other Fuels Savings Distribution"
                                            ),
                                            dbc.CardBody(
                                                [
                                                    html.Div(
                                                        dcc.Graph(
                                                            id="other-fuels-boxplot"
                                                        ),
                                                        className="chart-container boxplot-chart",
                                                    )
                                                ]
                                            ),
                                        ]
                                    )
                                ],
                                width=4,
                            ),
                        ]
                    ),
                    # SECTION: Investment Metrics
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H4(
                                    "Investment Metrics",
                                    className="section-header mt-4 mb-3",
                                ),
                                width=12,
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dbc.Card(
                                        [
                                            dbc.CardHeader(
                                                f"Implementation Cost Distribution ({reference_year} Year PPI-Adjusted Dollars)"
                                            ),
                                            dbc.CardBody(
                                                [
                                                    html.Div(
                                                        dcc.Graph(id="cost-boxplot"),
                                                        className="chart-container boxplot-chart",
                                                    )
                                                ]
                                            ),
                                        ]
                                    )
                                ],
                                width=6,
                            ),
                            dbc.Col(
                                [
                                    dbc.Card(
                                        [
                                            dbc.CardHeader(
                                                "Simple Payback Period Distribution"
                                            ),
                                            dbc.CardBody(
                                                [
                                                    html.Div(
                                                        dcc.Graph(id="payback-boxplot"),
                                                        className="chart-container boxplot-chart",
                                                    )
                                                ]
                                            ),
                                        ]
                                    )
                                ],
                                width=6,
                            ),
                        ]
                    ),
                    # SECTION: Emissions Metrics
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H4(
                                    "Emissions Metrics",
                                    className="section-header mt-4 mb-3",
                                ),
                                width=12,
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dbc.Card(
                                        [
                                            dbc.CardHeader(
                                                "Annual Reduction in Carbon Dioxide (CO2) Distribution"
                                            ),
                                            dbc.CardBody(
                                                [
                                                    html.Div(
                                                        dcc.Graph(id="co2-boxplot"),
                                                        className="chart-container boxplot-chart",
                                                    )
                                                ]
                                            ),
                                        ]
                                    )
                                ],
                                width=4,
                            ),
                            dbc.Col(
                                [
                                    dbc.Card(
                                        [
                                            dbc.CardHeader(
                                                "Annual Reduction in Sulphur Dioxide (SO2) Distribution"
                                            ),
                                            dbc.CardBody(
                                                [
                                                    html.Div(
                                                        dcc.Graph(id="so2-boxplot"),
                                                        className="chart-container boxplot-chart",
                                                    )
                                                ]
                                            ),
                                        ]
                                    )
                                ],
                                width=4,
                            ),
                            dbc.Col(
                                [
                                    dbc.Card(
                                        [
                                            dbc.CardHeader(
                                                "Annual Reduction in Nitrogen Oxides (NOx) Distribution"
                                            ),
                                            dbc.CardBody(
                                                [
                                                    html.Div(
                                                        dcc.Graph(id="nox-boxplot"),
                                                        className="chart-container boxplot-chart",
                                                    )
                                                ]
                                            ),
                                        ]
                                    )
                                ],
                                width=4,
                            ),
                        ]
                    ),
                ],
                width=12,
            ),
            # # SECTION: Table displaying an integrated dataset
            # dbc.Row([
            #     dbc.Col(html.H4("Assessment Recommendations Table", className="section-header text-primary mt-4 mb-3"), width=12)
            # ]),
            # dbc.Row([
            #     dbc.Col([
            #         dbc.Card([
            #             dbc.CardHeader("Assessment Recommendations Table"),
            #             dbc.CardBody([
            #                 html.Div(
            #                     dash_table.DataTable(
            #                         data=filters_df.head(10).to_dict('records'), # demo: display only 10 records
            #                         columns=[{"name": i, "id": i} for i in filters_df.columns],
            #                         style_table={'overflowX': 'scroll'},
            #                     ),
            #                     className="table-container"
            #                 )
            #             ])
            #         ])
            #     ], width=12, className="mb-4"),
            # ]),
        ],
        className="container-fluid p-4",
    )

    return create_base_layout(content)
