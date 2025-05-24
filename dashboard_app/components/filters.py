from dash import html, dcc
import dash_bootstrap_components as dbc


def create_filters(df):
    # Get unique values for each filter
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
                                        persistence=True,
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
                    # Middle - Outlier Filter Slider
                    dbc.Col(
                        [
                            html.Label(
                                "Outlier Exclusion Threshold (σ):",
                                className="filter-label",
                            ),
                            html.Div(
                                [
                                    dcc.Slider(
                                        id="outlier-filter",
                                        min=0,
                                        max=3,
                                        step=0.1,
                                        marks={0: "0σ", 1: "1σ", 2: "2σ", 3: "3σ"},
                                        value=2,  # Have 2σ automatic outlier filtering
                                        persistence=True,
                                        persistence_type="session",
                                        tooltip={
                                            "placement": "top",  # Consistent with FY slider
                                            "always_visible": True,  # Consistent with FY slider
                                        },
                                        className="custom-slider",
                                    )
                                ],
                                className="slider-container",
                            ),
                        ],
                        width=2,
                    ),
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
                                    persistence=True,
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
            # Second row - State, naics_description, and ARC filters
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
                                persistence=True,
                                persistence_type="session",
                                className="dash-dropdown",
                            ),
                        ],
                        width=2,
                    ),
                    # sector-description filter
                    dbc.Col(
                        [
                            html.Label("Sector:", className="filter-label"),
                            dcc.Dropdown(
                                id="sector-filter",
                                options=[
                                    {
                                        "label": f"{row['naics_imputed']} ({row['naics_description']})",
                                        "value": row["naics_imputed"],
                                    }
                                    for _, row in (
                                        df[["naics_imputed", "naics_description"]]
                                        .dropna()
                                        .drop_duplicates()
                                        .sort_values("naics_imputed")
                                        .iterrows()
                                    )
                                ],
                                placeholder="Select Sector",
                                multi=True,
                                value=["332812", "332813", "334418"],
                                persistence=True,
                                persistence_type="session",
                                className="dash-dropdown",
                            ),
                            html.Div(id="warning-message", style={"margin-top": "5px"}),
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
                                        "label": f"{row['arc2']} ({row['specific_description']})",
                                        "value": row["arc2"],
                                    }
                                    for _, row in (
                                        df[["arc2", "specific_description"]]
                                        .dropna()
                                        .drop_duplicates()
                                        .sort_values("arc2")
                                        .iterrows()
                                    )
                                ],
                                placeholder="Select Assessment Recommendation (ARC)",
                                multi=True,
                                value=["2.2511", "2.2514"],
                                persistence=True,
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


def filter_outliers(df, column_name, std_threshold=2):
    if df.empty or column_name not in df.columns:
        return df
    mean = df[column_name].mean()
    std = df[column_name].std()
    return df[
        (df[column_name] >= mean - std_threshold * std)
        & (df[column_name] <= mean + std_threshold * std)
    ]
