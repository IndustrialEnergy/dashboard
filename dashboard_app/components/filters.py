from dash import html, dcc
import dash_bootstrap_components as dbc


def create_filters(df):
    # Get unique values for each filter
    unique_sectors = sorted(df["sector"].dropna().unique())
    unique_states = sorted(df["state"].dropna().unique())

    return html.Div(
        [
            # First row - Year slider and Implementation Status
            dbc.Row(
                [
                    # Left side - Year Range Slider
                    dbc.Col(
                        [
                            html.Div(
                                html.Label(
                                    "Fiscal Year Range:",
                                    className="filter-label",
                                ),
                                className="mb-3",
                            ),
                            html.Div(
                                [
                                    dcc.RangeSlider(
                                        id="fy-filter",
                                        min=df["fy"].min(),
                                        max=df["fy"].max(),
                                        marks=None,
                                        value=[
                                            df["fy"].min(),
                                            df["fy"].max(),
                                        ],
                                        dots=False,
                                        step=1,
                                        allowCross=False,
                                        persistence_type="session",
                                        tooltip={
                                            "placement": "top",
                                            "always_visible": True,
                                        },
                                        className="custom-range-slider",
                                    )
                                ],
                                className="slider-container",
                            ),
                        ],
                        width=3,
                        className="d-flex flex-column",
                    ),
                    dbc.Col([
                        dbc.Checkbox(
                            id="outlier-filter",
                            className="form-check-input",
                            value=False,
                        ),
                        dbc.Label(
                            "Remove outliers (±2σ)",
                            html_for="outlier-filter",
                            className="form-check-label ms-2"
                        )
                    ], width=1),
                    # Right side - Implementation Status
                    dbc.Col(
                        [
                            html.Div(
                                html.Label(
                                    "Implementation Status:",
                                    className="filter-label",
                                ),
                                className="mb-3",
                            ),
                            html.Div(
                                dcc.Checklist(
                                    id="impstatus-filter",
                                    options=[
                                        {
                                            "label": html.Div(
                                                ["Implemented"],
                                                style={
                                                    "color": "Green",
                                                    "font-size": 15,
                                                    "padding-left": "5px",
                                                },
                                            ),
                                            "value": "I",
                                        },
                                        {
                                            "label": html.Div(
                                                ["Not Implemented"],
                                                style={
                                                    "color": "Red",
                                                    "font-size": 15,
                                                    "padding-left": "5px",
                                                },
                                            ),
                                            "value": "N",
                                        },
                                        {
                                            "label": html.Div(
                                                ["Pending"],
                                                style={
                                                    "color": "Black",
                                                    "font-size": 15,
                                                    "padding-left": "5px",
                                                },
                                            ),
                                            "value": "P",
                                        },
                                        {
                                            "label": html.Div(
                                                ["Unknown"],
                                                style={
                                                    "color": "Black",
                                                    "font-size": 15,
                                                    "padding-left": "5px",
                                                },
                                            ),
                                            "value": "K",
                                        },
                                    ],
                                    value=["I", "N"],
                                    labelStyle={
                                        "display": "flex",
                                        "align-items": "center",
                                    },
                                    inline=True,
                                    persistence_type="session",
                                    className="status-checklist",
                                ),
                                className="status-container",
                            ),
                        ],
                        width=4,
                        className="d-flex flex-column",
                    ),
                ],
                className="justify-content-center",
            ),
            # Second row - State, Sector, and ARC filters
            dbc.Row(
                [
                    # State filter
                    dbc.Col(
                        [
                            html.Label("State:", className="filter-label"),
                            dcc.Dropdown(
                                id="state-filter",
                                options=[
                                    {"label": str(val), "value": val}
                                    for val in unique_states
                                ],
                                placeholder="Select State",
                                multi=True,
                                value=["CA", "TX", "CO"],
                                persistence_type="session",
                                className="dash-dropdown",
                            ),
                        ],
                        width=2,
                    ),
                    # Sector filter
                    dbc.Col(
                        [
                            html.Label("Sector:", className="filter-label"),
                            dcc.Dropdown(
                                id="sector-filter",
                                options=[
                                    {"label": str(val), "value": val}
                                    for val in unique_sectors
                                ],
                                placeholder="Select Sector",
                                multi=True,
                                value=[
                                    "Metal Coating and Allied Services",
                                    "Electroplating, Plating, Polishing, Anodizing, and Coloring",
                                    "Printed Circuit Boards",
                                ],
                                persistence_type="session",
                                className="dash-dropdown",
                            ),
                        ],
                        width=5,
                    ),
                    # ARC filter
                    dbc.Col(
                        [
                            html.Label(
                                "Assessment Recommendation:", className="filter-label"
                            ),
                            dcc.Dropdown(
                                id="arc-filter",
                                options=[
                                    {
                                        "label": f"{row['arc2']} ({row['arc_description']})",
                                        "value": row["arc2"],
                                    }
                                    for _, row in (
                                        df[["arc2", "arc_description"]]
                                        .dropna()
                                        .drop_duplicates()
                                        .iterrows()
                                    )
                                ],
                                placeholder="Select Assessment Recommendation (ARC)",
                                multi=True,
                                value= ["2.2511", "2.2514"],
                                persistence_type="session",
                                className="dash-dropdown",
                            ),
                            html.Div(id="warning-message", style={"margin-top": "5px"}),
                        ],
                        width=5,
                    ),
                ],
                className="mb-2",
            ), 
        ],
        className="filter-container",
    )
