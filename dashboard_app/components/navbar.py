from dash import html
import dash_bootstrap_components as dbc
import os

def create_navbar():
    
    return html.Nav(
        className="navbar navbar-expand-lg navbar-dark bg-dark",
        children=[
            html.Div(
                className="container-fluid",
                children=[
                    html.A(
                        html.Img(
                            src='assets/isalab-logo.png',
                            height="30px",
                            style={'objectFit': 'contain'}
                        ),
                        className="navbar-brand",
                        href="/"
                    ),
                    # Navbar Toggle Button
                    dbc.NavbarToggler(id="navbar-toggler"),
                    
                    # Navbar Content
                    dbc.Collapse(
                        id="navbar-collapse",
                        is_open=False,
                        navbar=True,
                        children=[
                            dbc.Nav([
                                dbc.NavItem(dbc.NavLink("About", href="/about")),
                                dbc.NavItem(dbc.NavLink("Dashboard", href="/dashboard")),
                                dbc.NavItem(dbc.NavLink("Data", href="/data")),
                                dbc.NavItem(dbc.NavLink("Documentation", href="/documentation"))
                            ], navbar=True)
                        ]
                    )
                ]
            )
        ]
    )