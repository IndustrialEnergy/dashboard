import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

import os
import dash
from dash import Dash, dcc, html, Input, Output, callback
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

# import pages
from data_loader import load_integrated_dataset

from dashboard_app.pages.home_page import create_home_page
from dashboard_app.pages.about_page import create_about_page
from dashboard_app.pages.dashboard_page import create_dashboard_page
from dashboard_app.pages.docs_page import create_docs_page
from dashboard_app.pages.data_page import create_data_page
from dashboard_app.pages.contact_page import create_contact_page

# import callbacks
from dashboard_app.callbacks.cost_boxplot_callback import cost_boxplot_callback
from dashboard_app.callbacks.payback_boxplot_callback import payback_boxplot_callback
from dashboard_app.callbacks.arc_filter_limit_callback import arc_filter_limit_callback
from dashboard_app.callbacks.emissions_co2_callback import emissions_co2_callback
from dashboard_app.callbacks.emissions_so2_callback import emissions_so2_callback
from dashboard_app.callbacks.emissions_nox_callback import emissions_nox_callback
from dashboard_app.callbacks.electricity_boxplot_callback import emissions_electricity_callback
from dashboard_app.callbacks.fuels_boxplot_callback import emissions_fuels_callback
from dashboard_app.callbacks.download_buttons_callback import download_csv
from dashboard_app.callbacks.download_buttons_callback import download_excel

# Import components for download callback
from dashboard_app.components.download_buttons import get_data_from_zip

def create_app():
    # get absolute path to assets folder
    assets_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "assets")
    )

    app = Dash(
        __name__,
        external_stylesheets=[
            dbc.themes.BOOTSTRAP,
            "https://use.fontawesome.com/releases/v5.15.4/css/all.css",
            "https://fonts.googleapis.com/css2?family=Oswald:wght@400;700&family=Montserrat:wght@400;500;600;700&family=Poppins:wght@400;500&family=Inter:wght@400;500&display=swap",
        ],
        suppress_callback_exceptions=True,
        assets_folder=assets_path,  # set absolute path to assets
        assets_url_path="assets",  # explicitly set the assets URL path
    )

    # load data
    integrated_df = load_integrated_dataset()
    print(integrated_df.shape)
    print(integrated_df.info())

    filters_df = integrated_df[
        ["fy", "sector", "state", "arc2", "arc_description", "impstatus"]
    ]
    boxplot_cost_df = integrated_df[
        ["fy", "sector", "state", "arc2", "arc_description", "impstatus", "impcost_adj"]
    ]
    boxplot_payback_df = integrated_df[
        ["fy", "sector", "state", "arc2", "arc_description", "impstatus", "payback"]
    ]
    boxplot_co2_df = integrated_df[integrated_df['emission_type'] == "CO2"][
        ["fy", "sector", "state", "arc2", "arc_description", "impstatus", "emissions_avoided"]
    ]
    boxplot_nox_df = integrated_df[integrated_df['emission_type'] == "NOx"][
        ["fy", "sector", "state", "arc2", "arc_description", "impstatus", "emissions_avoided"]
    ]
    boxplot_so2_df = integrated_df[integrated_df['emission_type'] == "SO2"][
        ["fy", "sector", "state", "arc2", "arc_description", "impstatus", "emissions_avoided"]
    ]
    boxplot_electricity_df = integrated_df[integrated_df['sourccode'].isin(["EC", "ED", "EF"])][
        ["fy", "sector", "state", "arc2", "arc_description", "impstatus", "conserved"]
    ]
    boxplot_fuels_df = integrated_df[~integrated_df['sourccode'].isin(["EC", "ED", "EF"])][
        ["fy", "sector", "state", "arc2", "arc_description", "impstatus", "conserved"]
    ]
    # initialize callbacks
    cost_boxplot_callback(app, boxplot_cost_df)
    payback_boxplot_callback(app, boxplot_payback_df)
    emissions_co2_callback(app, boxplot_co2_df)
    emissions_so2_callback(app, boxplot_so2_df)
    emissions_nox_callback(app, boxplot_nox_df)
    emissions_electricity_callback(app, boxplot_electricity_df)
    emissions_fuels_callback(app, boxplot_fuels_df)
    arc_filter_limit_callback(app)
    download_excel(app, get_data_from_zip)
    download_csv(app)

    # URL routing
    app.layout = html.Div(
        [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
    )

    @app.callback(Output("page-content", "children"), Input("url", "pathname"))
    def display_page(pathname):
        print(f"\nRouting request for pathname: {pathname}")  # Debug print
        if pathname == "/home":
            return create_home_page()
        if pathname == "/about":
            return create_about_page()
        elif pathname == "/dashboard":
            return create_dashboard_page(
                filters_df
            ) 
        elif pathname == "/documentation":
            return create_docs_page()
        elif pathname == "/data":
            return create_data_page()
        elif pathname == "/contact":
            return create_contact_page()
        else:
            print(f"No route match, defaulting to home page")  # debug print
            return create_home_page()

    # navbar toggle callback
    @app.callback(
        Output("navbar-collapse", "is_open"),
        [Input("navbar-toggler", "n_clicks")],
        [State("navbar-collapse", "is_open")],
    )
    def toggle_navbar_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    return app


if __name__ == "__main__":
    app = create_app()
    app.run_server(debug=True)
