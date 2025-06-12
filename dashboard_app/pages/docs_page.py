from dash import html, dcc
import dash_bootstrap_components as dbc
from layouts.base_layout import create_base_layout


# def create_docs_page():
#     content = html.Div(
#         [
#             # Header Section
#             dbc.Row(
#                 [
#                     dbc.Col(
#                         [
#                             html.H3(
#                                 "Documentation",
#                                 className="d-flex landing-page-title justify-content-center mb-4 mt-4",
#                             ),
#                         ]
#                     )
#                 ]
#             ),
#             # User Guide Card Section
#             dbc.Row(
#                 [
#                     dbc.Col(
#                         [
#                             dbc.Card(
#                                 [
#                                     dbc.CardHeader(
#                                         [
#                                             html.H5(
#                                                 "User Guide",
#                                                 className="mb-0",
#                                                 style={
#                                                     "color": "#003660",
#                                                     "fontWeight": "bold",
#                                                 },
#                                             )
#                                         ]
#                                     ),
#                                     dbc.CardBody(
#                                         [
#                                             html.P(
#                                                 [
#                                                     "Download the comprehensive user guide to learn how to navigate and use all features of the Industrial Energy Dashboard. ",
#                                                     "This guide includes step-by-step instructions, feature explanations, and best practices for data exploration.",
#                                                 ],
#                                                 className="card-text mb-3",
#                                             ),
#                                             html.Div(
#                                                 [
#                                                     dbc.Button(
#                                                         [
#                                                             html.I(
#                                                                 className="fas fa-download me-2"
#                                                             ),
#                                                             "Download User Guide (PDF)",
#                                                         ],
#                                                         id="btn-ug-download-pdf",
#                                                         color="primary",
#                                                         size="lg",
#                                                         className="d-flex align-items-center justify-content-center",
#                                                     )
#                                                 ],
#                                                 className="d-grid",
#                                             ),
#                                             # Download component
#                                             dcc.Download(id="download-pdf"),
#                                         ]
#                                     ),
#                                 ],
#                                 className="mb-4 border-start border-primary border-3 shadow-sm",
#                             )
#                         ],
#                         md=8,
#                         lg=6,
#                         className="mx-auto",
#                     )
#                 ]
#             ),
#             # Tech Doc Card Section
#             dbc.Row(
#                 [
#                     dbc.Col(
#                         [
#                             dbc.Card(
#                                 [
#                                     dbc.CardHeader(
#                                         [
#                                             html.H5(
#                                                 "Technical Documentation",
#                                                 className="mb-0",
#                                                 style={
#                                                     "color": "#003660",
#                                                     "fontWeight": "bold",
#                                                 },
#                                             )
#                                         ]
#                                     ),
#                                     dbc.CardBody(
#                                         [
#                                             html.P(
#                                                 [
#                                                     "Download the comprehensive technical documentation on the creation and implementation processes of our Capstone project - from integrating the dataset to creating the dashboard."
#                                                 ],
#                                                 className="card-text mb-3",
#                                             ),
#                                             html.Div(
#                                                 [
#                                                     dbc.Button(
#                                                         [
#                                                             html.I(
#                                                                 className="fas fa-download me-2"
#                                                             ),
#                                                             "Download User Guide (PDF)",
#                                                         ],
#                                                         id="btn-td-download-pdf",
#                                                         color="primary",
#                                                         size="lg",
#                                                         className="d-flex align-items-center justify-content-center",
#                                                     )
#                                                 ],
#                                                 className="d-grid",
#                                             ),
#                                             # Download component
#                                             dcc.Download(id="download-pdf"),
#                                         ]
#                                     ),
#                                 ],
#                                 className="mb-4 border-start border-primary border-3 shadow-sm",
#                             )
#                         ],
#                         md=8,
#                         lg=6,
#                         className="mx-auto",
#                     )
#                 ]
#             ),
#         ]
#     )

#     return create_base_layout(content)


def create_docs_page():
    content = html.Div(
        [
            # User Manuals Section
            html.H3("User Manuals", className="text-center mb-2 pb-3"),
            # Dashboard User Manual Card
            html.Div(
                [
                    html.A(
                        [
                            html.H5("Dashboard User Manual (PDF)", className="mb-1"),
                            html.P(
                                "Learn how to navigate and use the dashboard",
                                className="mb-0 text-muted",
                            ),
                        ],
                        href="/assets/User_Guide.pdf",
                        target="_blank",
                        className="guide-card",
                    )
                ],
                className="mb-3",
            ),
            # Technical Documentation Card
            html.Div(
                [
                    html.A(
                        [
                            html.H5("Technical Documentation (PDF)", className="mb-1"),
                            html.P(
                                "Dashboard development and implementation details",
                                className="mb-0 text-muted",
                            ),
                        ],
                        href="/assets/Technical_Documentation.pdf",
                        target="_blank",
                        className="guide-card",
                    )
                ],
                className="mb-4",
            ),
            html.H3("Developer Guides", className="text-center mb-2 pb-3"),
            # Installation Guide Card
            html.Div(
                [
                    html.A(
                        [
                            html.H5("📦 Installation Guide", className="mb-1"),
                            html.P(
                                "Set up the dashboard on your local machine",
                                className="mb-0 text-muted",
                            ),
                        ],
                        href="/assets/docs/dashboard_installation_guide.html",
                        className="guide-card",
                    )
                ],
                className="mb-3",
            ),
            # Data Update Guide Card
            html.Div(
                [
                    html.A(
                        [
                            html.H5("🔄 Data Update Guide", className="mb-2"),
                            html.Ul(
                                [
                                    html.Li(
                                        "Generate integrated datasets for your own analysis"
                                    ),
                                    html.Li("Refresh the dashboard with latest data"),
                                ],
                                className="mb-0 text-muted",
                                style={"fontSize": "0.9em"},
                            ),
                        ],
                        href="/assets/docs/data_update_guide.html",
                        className="guide-card",
                    )
                ],
                className="mb-3",
            ),
            # Dashboard Update Guide Card
            html.Div(
                [
                    html.A(
                        [
                            html.H5("⬆️ Dashboard Update Guide", className="mb-1"),
                            html.P(
                                "Add new visualizations and components to the dashboard",
                                className="mb-0 text-muted",
                            ),
                        ],
                        href="/assets/docs/update_dashboard_guide.html",
                        className="guide-card",
                    )
                ],
                className="mb-4",
            ),
            html.Hr(),
            html.P(
                "New to the dashboard? Start with the Dashboard User Manual",
            ),
        ],
        style={"maxWidth": "800px", "margin": "0 auto", "padding": "20px"},
    )

    return create_base_layout(content)
