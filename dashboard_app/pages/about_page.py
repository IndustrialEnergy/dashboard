from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from layouts.base_layout import create_base_layout
from components.filters import create_filters

def create_about_page():
    content = html.Div([
        dbc.Row([
            dbc.Col(
                html.H3("Learn More About:"),
                className="d-flex landing-page-title justify-content-center mb-4 mt-4",
            )
        ]),
        # First Row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6(
                            "The Dashboard",
                            className="card-title mb-2",
                            style={"color": "#003660"},
                        ),
                        dcc.Markdown(
                            "This dashboard presents a centralized interface for exploring industrial energy audit data, including potential and realized energy savings across facilities and recommendations. It is designed to support data exploration, policy analysis, and decarbonization strategies in industrial energy use. This dashboard has been created as a [Capstone](https://bren.ucsb.edu/masters-programs/master-environmental-data-science/meds-capstone-projects) project deliverable for the [Masters of Environmental Data Science](https://bren.ucsb.edu/masters-programs/master-environmental-data-science) from the [Bren School of Environmental Science & Management](https://bren.ucsb.edu/) at the [University of California, Santa Barbara](https://www.ucsb.edu/)."
                        ),
                    ])
                ], className="mb-3 border-start border-secondary border-1"),
            ], md=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6(
                            "The Team",
                            className="card-title mb-2",
                            style={"color": "#003660"},
                        ),
                        dcc.Markdown(
                            "The Capstone team behind the dashboard is the Industrial Energy student team, composed of the following members: Oksana Protsukha, Naomi Moraes, Eva Newby, and Yos Ramirez. This project was completed with the support and guidance of our client and faculty advisor, [Dr. Eric Masanet](https://bren.ucsb.edu/people/eric-masanet). Dr. Masanet heads the Industrial Sustainability Analysis Laboratory at the University of California, Santa Barbara. Dr. Masanet is also a teaching professor and holds the Mellichamp Chair in Sustainability Science for Emerging Technologies in the Bren School as well as committee member for [Industrial Technology Innovation Advisory Committee](https://www.energy.gov/eere/iedo/industrial-technology-innovation-advisory-committee) at the [U.S. Department of Energy](https://www.energy.gov/)."
                        ),
                    ])
                ], className="mb-3 border-start border-secondary border-1"),
            ], md=6),
        ]),
        
        # Second Row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6(
                            "The Data",
                            className="card-title mb-2",
                            style={"color": "#003660"},
                        ),
                        dcc.Markdown(
                            "The integrated dataset that powers the dashboard is derived from the following sources: [Industrial Assessment Center - Database](https://iac.university/download), [Environmental Protection Agency - AP-42: Compilation of of Air Emissions Factors from Stationary Factors](https://www.epa.gov/air-emissions-factors-and-quantification/ap-42-compilation-air-emissions-factors-stationary-sources), [U.S. Energy Information Administration - Electricity Emissions and Generation Data](https://www.eia.gov/electricity/data.php), and [U.S. Bureau of Labor Statistics - Producer Price Indexes](https://www.eia.gov/electricity/data.php)."
                        ),
                    ])
                ], className="mb-3 border-start border-secondary border-1"),
            ], md=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6(
                            "Access",
                            className="card-title mb-2",
                            style={"color": "#003660"},
                        ),
                        dcc.Markdown(
                            "The GitHub repository associated with this dashboard can be found [here](IndustrialEnergy/.github). The GitHub repository contains all information on producing the integrated dataset and deploying the dashboard, should new data become available. Our data, code, and processes are open-source - in keeping with Bren's commitment to transparent and collaborative environmental data practices."
                        ),
                    ])
                ], className="mb-3 border-start border-secondary border-1"),
            ], md=6),
        ])
    ])
    
    return create_base_layout(content)