from dash import html, dcc
import dash_bootstrap_components as dbc

def create_filters(df):

    return dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id="naics-filter",
                options=[{"label": str(val), "value": val} for val in sorted(df["naics"].dropna().unique())],
                placeholder="Select NAICS",
                multi=True
            )
        ], width=3),

        dbc.Col([
            dcc.Dropdown(
                id="fy-filter",
                options=[{"label": str(val), "value": val} for val in sorted(df["fy"].dropna().unique())],
                placeholder="Select Fiscal Year",
                multi=True
            )
        ], width=3),

        # dbc.Col([
        #     dcc.Checklist(
        #         id="impstatus-filter",
        #         options=[{"label": str(val), "value": val} for val in sorted(df["impstatus"].dropna().unique())],
        #         value=["N","I"],
        #         #labelStyle={"display": "inline-block", "marginRight": "10px"},
        #     )
        # ], #width=3
        # ),

        dbc.Col([
            dcc.Checklist(
                id = "impstatus-filter",
                options = [
                    {
                        "label": html.Div(['Implemented'], style={'color': 'Green', 'font-size': 15, "padding-left" :"5px"}),
                        "value": "I",
                    },
                    {
                        "label": html.Div(['Not Implemented'], style={'color': 'Red', 'font-size': 15, "padding-left" :"5px"}),
                        "value": "N",
                    },
                    {
                        "label": html.Div(['Pending'], style={'color': 'Black', 'font-size': 15, "padding-left" :"5px"}),
                        "value": "P",
                    },
                    {
                        "label": html.Div(['Uknwown'], style={'color': 'Black', 'font-size': 15, "padding-left" :"5px"}),
                        "value": "K",
                    },
                ], 
                value = ['I', 'N'],
                labelStyle = {"display": "flex", "align-items": "center"}
            ),
        ], width=2),

        dbc.Col([
            dcc.Dropdown(
                id="arc2-filter",
                options=[{"label": val, "value": val} for val in sorted(df["arc2"].dropna().unique())],
                placeholder="Select ARC2",
                multi=True
            )
        ], width=3),
    ], className="mb-5")
