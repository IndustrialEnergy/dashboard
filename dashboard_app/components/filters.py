from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from pathlib import Path

# Import utility functions from helpers
from dashboard_app.helpers.get_naics_descriptions import get_naics_descriptions
from dashboard_app.helpers.get_wildcard_patterns import get_wildcard_patterns
from dashboard_app.helpers.filter_outliers import filter_outliers
from dashboard_app.helpers.apply_wildcard_filter import apply_wildcard_filter


def create_filters(df):
    # Get unique values for each filter
    unique_states = sorted(df["state"].dropna().unique())
    unique_arc_codes = sorted(df["arc2"].dropna().unique())
    unique_naics_codes = sorted(df["naics_imputed"].dropna().unique())

    # Generate wildcard options
    arc_wildcards = get_wildcard_patterns(unique_arc_codes, "arc", df)
    naics_wildcards = get_wildcard_patterns(unique_naics_codes, "naics")

    # Debug: Print what wildcards are being generated
    print(f"Generated ARC wildcards: {[w['label'] for w in arc_wildcards]}")
    print(f"Generated NAICS wildcards: {[w['label'] for w in naics_wildcards]}")
    print(
        f"Sample NAICS codes in data: {sorted(unique_naics_codes)[:10]}"
    )  # First 10 codes

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
            # Second row - Sector, ARC, then State (reordered)
            dbc.Row(
                [
                    # Sector filter - MOVED TO FIRST
                    dbc.Col(
                        [
                            html.Label("Sector:", className="filter-label"),
                            dcc.Dropdown(
                                id="sector-filter",
                                options=naics_wildcards
                                + [
                                    {
                                        "label": f"{row['naics_imputed']} - {row['naics_description']}",
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
                                placeholder="All sectors",  # UPDATED PLACEHOLDER
                                multi=True,
                                value=["332812", "332813", "334418"],
                                persistence=True,
                                persistence_type="session",
                                className="dash-dropdown",
                            ),
                            html.Div(id="warning-message", style={"margin-top": "5px"}),
                        ],
                        width=4,
                    ),
                    # ARC filter - MOVED TO SECOND
                    dbc.Col(
                        [
                            html.Label(
                                "Assessment Recommendation:", className="filter-label"
                            ),
                            dcc.Dropdown(
                                id="arc-filter",
                                options=arc_wildcards
                                + [
                                    {
                                        "label": f"{row['arc2']} - {row['specific_description']}",
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
                                placeholder="All recommendations",  # UPDATED PLACEHOLDER
                                multi=True,
                                value=["2.2511", "2.2514"],
                                persistence=True,
                                persistence_type="session",
                                className="dash-dropdown",
                            ),
                        ],
                        width=5,
                    ),
                    # State filter - MOVED TO THIRD
                    dbc.Col(
                        [
                            html.Label("State:", className="filter-label"),
                            dcc.Dropdown(
                                id="state-filter",
                                options=[
                                    {"label": str(val), "value": val}
                                    for val in unique_states
                                ],
                                placeholder="All states",  # UPDATED PLACEHOLDER
                                multi=True,
                                value=["CA", "TX", "CO"],
                                persistence=True,
                                persistence_type="session",
                                className="dash-dropdown",
                            ),
                        ],
                        width=3,
                    ),
                ],
                className="mb-2",
            ),
        ],
        className="filter-container",
    )
