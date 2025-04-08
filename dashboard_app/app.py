import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

import os
import dash
from dash import Dash, dcc, html, Input, Output, callback
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

# ✅ Updated local module imports
from dashboard_app.data_loader import load_integrated_dataset

from dashboard_app.pages.home_page import create_home_page
from dashboard_app.pages.about_page import create_about_page
from dashboard_app.pages.dashboard_page import create_dashboard_page
from dashboard_app.pages.docs_page import create_docs_page
from dashboard_app.pages.data_page import create_data_page
from dashboard_app.pages.contact_page import create_contact_page


def create_app():
    # Get absolute path to assets folder
    assets_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "assets")
    )

    # Debug logging
    print(f"Current working directory: {os.getcwd()}")
    print(f"Assets folder path: {assets_path}")
    print(f"Assets folder exists: {os.path.exists(assets_path)}")

    # List all files in assets directory
    print("\nFiles in assets directory:")
    for root, dirs, files in os.walk(assets_path):
        for file in files:
            file_path = os.path.join(root, file)

    app = Dash(
        __name__,
        external_stylesheets=[
            dbc.themes.BOOTSTRAP,
            "https://use.fontawesome.com/releases/v5.15.4/css/all.css",
            "https://fonts.googleapis.com/css2?family=Oswald:wght@400;700&family=Montserrat:wght@400;500;600;700&family=Poppins:wght@400;500&family=Inter:wght@400;500&display=swap",
        ],
        suppress_callback_exceptions=True,
        assets_folder=assets_path,  # Set absolute path to assets
        assets_url_path="assets",  # Explicitly set the assets URL path
    )

    # Load data
    integrated_df = load_integrated_dataset()

    # Initialize callbacks


    # URL Routing
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
            return create_dashboard_page()
        elif pathname == "/documentation":
            return create_docs_page()
        elif pathname == "/data":
            return create_data_page()
        elif pathname == "/contact":
            return create_contact_page()
        else:
            print(f"No route match, defaulting to home page")  # Debug print
            return create_home_page()

    # Navbar toggle callback - moved inside create_app()
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
