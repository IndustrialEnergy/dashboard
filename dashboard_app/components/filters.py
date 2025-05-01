from dash import html, dcc
import dash_bootstrap_components as dbc


def create_filters(df):
    return dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Dropdown(
                        id="fy-filter",
                        options=[
                            {"label": str(val), "value": val}
                            for val in sorted(df["fy"].dropna().unique())
                        ],
                        placeholder="Select Fiscal Year",
                        multi=True,
                    )
                ],
                width=3,
            ),
            dbc.Col(
                [
                    dcc.Dropdown(
                        id="state-filter",
                        options=[
                            {"label": str(val), "value": val}
                            for val in sorted(df["state"].dropna().unique())
                        ],
                        placeholder="Select State",
                        multi=True,
                        value= ["CA", "TX", "CO"]
                    )
                ],
                width=3,
            ),
            dbc.Col(
                [
                    dcc.Dropdown(
                        id="sector-filter",
                        options=[
                            {"label": str(val), "value": val}
                            for val in sorted(df["sector"].dropna().unique())
                        ],
                        placeholder="Select Sector",
                        multi=True,
                        value=["Metal Coating and Allied Services", "Electroplating, Plating, Polishing, Anodizing, and Coloring", "Printed Circuit Boards"],
                    )
                ],
                width=3,
            ),
            dbc.Col(
                [
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
                    ),
                    html.Div(id="warning-message", style={"margin-top": "5px"}),
                ],
                width=3,
            ),
            dbc.Col(
                [
                    html.H5(
                        "Implementation Status:",
                        style={"font-size": 20, "padding-top": "20px"},
                    ),
                    dcc.Checklist(
                        id="impstatus-filter",
                        options=[
                            {"label": "Implemented", "value": "I"},
                            {"label": "Not Implemented", "value": "N"},
                            {"label": "Pending", "value": "P"},
                            {"label": "Unknown", "value": "K"},
                        ],
                        value=["I", "N"],
                        labelStyle={
                            "padding": "5px",
                        },
                        inline=True,
                    ),
                ],
                width=6,
            ),
        ],
        className="mb-5",
    )
