from dash import html, dcc
import dash_bootstrap_components as dbc
from layouts.base_layout import create_base_layout
import pandas as pd


def create_data_page():
    content = html.Div(
        [
            # Header Section
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H3("Data Overview", className="text-center mb-2"),
                            html.P(
                                "This dashboard integrates publicly available datasets from government agencies and research institutions to provide comprehensive insights into industrial energy efficiency. All sources are free of intellectual property restrictions and non-disclosure agreements.",
                                className="text-center text-muted mb-4",
                            ),
                        ],
                        width=10,  # Change to match other sections
                        className="px-5",  # Keep the px-5 for consistency
                    )
                ],
                justify="center",  # Add centering to match other sections
            ),
            # Download Section - Moved to Top
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H5(
                                "📥 Download Integrated Dataset",
                                className="text-center mb-3",
                            ),
                            html.Div(
                                [
                                    dbc.Button(
                                        [
                                            html.I(className="fas fa-file-excel me-2"),
                                            "Download Excel",
                                        ],
                                        id="btn-download-excel",
                                        color="success",
                                        size="lg",
                                        className="me-3",
                                    ),
                                    dbc.Button(
                                        [
                                            html.I(className="fas fa-file-csv me-2"),
                                            "Download CSV",
                                        ],
                                        id="btn-download-csv",
                                        color="secondary",
                                        size="lg",
                                    ),
                                ],
                                className="d-flex justify-content-center mb-4",
                            ),
                            # Tooltips and download components
                            dbc.Tooltip(
                                "Download integrated dataset as Excel file",
                                target="btn-download-excel",
                            ),
                            dbc.Tooltip(
                                "Download integrated dataset as CSV file",
                                target="btn-download-csv",
                            ),
                            dcc.Download(id="download-excel"),
                            dcc.Download(id="download-csv"),
                        ],
                        width=10,
                        className="px-5",
                    )
                ],
                justify="center",
            ),
            # Data Integration Flow Diagram
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H5(
                                "Data Integration Diagram", className="text-center mb-3"
                            ),
                            html.Div(
                                [
                                    html.Img(
                                        src="/assets/IndustrialEnergy-DataMapping.svg",
                                        style={
                                            "width": "100%",
                                            "max-width": "1200px",
                                            "height": "auto",
                                            "cursor": "pointer",
                                        },
                                        className="img-fluid",
                                        id="data-flow-diagram",
                                    )
                                ],
                                className="text-center mb-3",
                            ),
                            html.P(
                                "Click diagram to zoom",
                                className="text-center text-muted small mb-5",
                            ),
                            # Modal for zoomed diagram
                            dbc.Modal(
                                [
                                    dbc.ModalHeader(
                                        dbc.ModalTitle("Data Integration Diagram")
                                    ),
                                    dbc.ModalBody(
                                        [
                                            html.Img(
                                                src="/assets/IndustrialEnergy-DataMapping.svg",
                                                style={
                                                    "width": "100%",
                                                    "height": "auto",
                                                    "max-width": "none",  # Remove max-width constraint
                                                    "min-width": "800px",  # Ensure minimum size
                                                },
                                                className="img-fluid",
                                            )
                                        ],
                                        style={
                                            "overflow": "auto"
                                        },  # Allow scrolling if needed
                                    ),
                                    dbc.ModalFooter(
                                        dbc.Button(
                                            "Close",
                                            id="close-diagram-modal",
                                            className="ms-auto",
                                            n_clicks=0,
                                        )
                                    ),
                                ],
                                id="diagram-modal",
                                is_open=False,
                                size="xl",
                                fullscreen=True,  # Make modal fullscreen for better zoom experience
                            ),
                        ],
                        width=12,
                        className="px-5",  # Add same margins as rest of page
                    )
                ]
            ),
            # Field Definitions Section (moved above Data Sources)
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H4("Field Definitions", className="mb-3 text-center"),
                            # Complete Field Definitions
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.H6(
                                                "Original IAC Assessment Fields",
                                                className="mb-3 text-center",
                                            ),
                                            html.Ul(
                                                [
                                                    html.Li(
                                                        [
                                                            html.Strong("id"),
                                                            " - Assessment ID",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("center"),
                                                            " - IAC Center Code",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("fy"),
                                                            " - Fiscal year in which the assessment was conducted",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("sic"),
                                                            " - SIC industrial classification code",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("naics"),
                                                            " - NAICS industrial classification code",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("state"),
                                                            " - US State abbreviation",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("sales"),
                                                            " - Total yearly sales",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("employees"),
                                                            " - Total site employees",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("plant_area"),
                                                            " - Total plant square footage",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("products"),
                                                            " - Types of products",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("produnits"),
                                                            " - Production level units",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("prodlevel"),
                                                            " - Total yearly production",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("prodhours"),
                                                            " - Total yearly hours of operation",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("numars"),
                                                            " - Total number of recommendations",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("sourccode"),
                                                            " - Type of energy source",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("plant_cost"),
                                                            " - Total yearly electricity consumption costs ($)",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("plant_usage"),
                                                            " - Total yearly electricity consumption (kWh)",
                                                        ]
                                                    ),
                                                ],
                                                className="small",
                                            ),
                                        ],
                                        md=6,
                                    ),
                                    dbc.Col(
                                        [
                                            html.H6(
                                                "Original IAC Recommendation Fields",
                                                className="mb-3 text-center",
                                            ),
                                            html.Ul(
                                                [
                                                    html.Li(
                                                        [
                                                            html.Strong("superid"),
                                                            " - Assessment ID + Recommendation Number",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("ar_number"),
                                                            " - Recommendation Number",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("appcode"),
                                                            " - Application Code",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("arc2"),
                                                            " - IAC Assessment Recommendation Code",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("impstatus"),
                                                            " - Implementation Status (I = implemented, N = Not Implemented)",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("impcost"),
                                                            " - Total implementation cost",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("source_rank"),
                                                            " - Rank of the energy source (Primary, Secondary, Tertiary, Quaternary)",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("conserved"),
                                                            " - The amount of energy resource conserved",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("sourconsv"),
                                                            " - Energy consumed at the source needed to produce consumed energy at site",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("saved"),
                                                            " - Cost savings",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("rebate"),
                                                            " - Was a rebate involved (yes/no)",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("incremntal"),
                                                            " - Was the recommendation implemented incrementally (yes/no)",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("ic_capital"),
                                                            " - Capital component of implementation cost",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("ic_other"),
                                                            " - Other component of implementation cost",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("payback"),
                                                            " - Simple Payback (years)",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("bptool"),
                                                            " - What best practice tools was used (if any)",
                                                        ]
                                                    ),
                                                ],
                                                className="small",
                                            ),
                                        ],
                                        md=6,
                                    ),
                                ],
                                className="mb-4 justify-content-center",
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.H6(
                                                "New Calculated Fields",
                                                className="mb-3 text-center",
                                            ),
                                            html.Ul(
                                                [
                                                    html.Li(
                                                        [
                                                            html.Strong(
                                                                "payback_imputed"
                                                            ),
                                                            " - Estimated payback value, calculated as saved / impcost_adj",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong(
                                                                "emissions_avoided"
                                                            ),
                                                            " - Estimated emissions avoided, calculated as Emission Factor × Conserved",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong(
                                                                "emission_type"
                                                            ),
                                                            " - Type of emitted pollutant (e.g., CO₂, SO₂, NOₓ)",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong(
                                                                "emission_factor_units"
                                                            ),
                                                            " - Units associated with the emission factor value",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong(
                                                                "emission_factor"
                                                            ),
                                                            " - Emission factor used for calculating avoided emissions",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("base_year"),
                                                            " - Base year for the recommendation, used to adjust implementation costs using PPI",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong(
                                                                "reference_year"
                                                            ),
                                                            " - Latest available PPI year used to adjust implementation costs",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong(
                                                                "reference_ppi"
                                                            ),
                                                            " - PPI value for the recommendation category in the reference year",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("base_ppi"),
                                                            " - PPI value for the recommendation category in the base year",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("impcost_adj"),
                                                            " - Implementation cost adjusted to the base year using PPI",
                                                        ]
                                                    ),
                                                ],
                                                className="small",
                                            ),
                                        ],
                                        md=6,
                                    ),
                                    dbc.Col(
                                        [
                                            html.H6(
                                                "Classification & Code Fields",
                                                className="mb-3 text-center",
                                            ),
                                            html.Ul(
                                                [
                                                    html.Li(
                                                        [
                                                            html.Strong("main_code"),
                                                            " - Main ARC code (e.g., 2.3); 2-digit recommendation category code",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong(
                                                                "main_description"
                                                            ),
                                                            " - Description of the main ARC code (e.g., Electrical Power)",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("sub_code"),
                                                            " - Sub ARC code (e.g., 2.32); 3-digit recommendation category code",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong(
                                                                "sub_description"
                                                            ),
                                                            " - Description of the sub ARC code (e.g., Power Factor)",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong("detail_code"),
                                                            " - Detail ARC code (e.g., 2.321); 4-digit recommendation category code",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong(
                                                                "detail_description"
                                                            ),
                                                            " - Description of the detail ARC code (e.g., General)",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong(
                                                                "specific_code"
                                                            ),
                                                            " - Specific ARC code (e.g., 2.3212); 5-digit detailed recommendation code",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong(
                                                                "specific_description"
                                                            ),
                                                            " - Description of the specific ARC code (e.g., Optimize Plant Power Factor)",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong(
                                                                "naics_imputed"
                                                            ),
                                                            " - NAICS code filled when missing by looking up SIC code;",
                                                            html.Br(),
                                                            "otherwise retains original NAICS code",
                                                        ]
                                                    ),
                                                    html.Li(
                                                        [
                                                            html.Strong(
                                                                "naics_description"
                                                            ),
                                                            " - Industry description corresponding to the NAICS code",
                                                        ]
                                                    ),
                                                ],
                                                className="small",
                                            ),
                                        ],
                                        md=6,
                                    ),
                                ],
                                className="justify-content-center",
                            ),
                        ],
                        width=10,
                        className="px-5",  # Add same margins as rest of page
                    )
                ],
                justify="center",
            ),
            # Data Sources Section (Non-collapsible)
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H4("Data Sources", className="mb-4 text-center"),
                            # Dataset 1: Industrial Energy Audits
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.H6(
                                                "Industrial Energy Audits Database",
                                                className="card-title mb-2",
                                                style={"color": "#003660"},
                                            ),
                                            html.P(
                                                "Database containing technical information about more than 13,000 industrial energy audits done by all the industrial assessment centers. This includes information on the type of facility assessed (size, industry, energy usage, etc.) and details of resulting recommendations (type, energy & dollar savings etc.).",
                                                className="mb-2",
                                            ),
                                            html.Ul(
                                                [
                                                    html.Li(
                                                        "Assess table: 30 variables per industrial audit assessment"
                                                    ),
                                                    html.Li(
                                                        "Recommendation table: 55 variables per energy efficiency recommendation"
                                                    ),
                                                    html.Li(
                                                        "Technical details and data point descriptions available on the IAC website"
                                                    ),
                                                ],
                                                className="mb-2",
                                            ),
                                            html.Div(
                                                [
                                                    dbc.Badge(
                                                        "Excel 2003 (.xls)",
                                                        color="light",
                                                        text_color="dark",
                                                        className="me-2",
                                                    ),
                                                    dbc.Badge(
                                                        "13.2 MB",
                                                        color="light",
                                                        text_color="dark",
                                                        className="me-2",
                                                    ),
                                                ],
                                                className="mb-2",
                                            ),
                                            html.Small(
                                                [
                                                    "Source: ",
                                                    html.A(
                                                        "U.S. Department of Energy - Industrial Assessment Centers",
                                                        href="https://iac.university/download",
                                                        target="_blank",
                                                        style={"color": "#003660"},
                                                    ),
                                                    " | ",
                                                    html.A(
                                                        "Database Documentation",
                                                        href="https://iac.university/#database",
                                                        target="_blank",
                                                        style={"color": "#003660"},
                                                    ),
                                                ],
                                                className="text-muted",
                                            ),
                                        ]
                                    )
                                ],
                                className="mb-3 border-start border-secondary border-1",
                            ),
                            # Dataset 2: Electric Power Emissions
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.H6(
                                                "Electric Power Emissions and Air Pollutants",
                                                className="card-title mb-2",
                                                style={"color": "#003660"},
                                            ),
                                            html.P(
                                                "National and regional data on electricity generating capacity, electricity generation and useful thermal output, fuel receipts, consumption, and emissions. The dataset is used to determine air pollutant emission quantities (CO₂, SOₓ, NOₓ, etc.) avoided by energy efficiency recommendations that lead to electricity savings.",
                                                className="mb-2",
                                            ),
                                            html.Div(
                                                [
                                                    dbc.Badge(
                                                        "Excel (.xlsx)",
                                                        color="light",
                                                        text_color="dark",
                                                        className="me-2",
                                                    ),
                                                    dbc.Badge(
                                                        "2.1 MB",
                                                        color="light",
                                                        text_color="dark",
                                                        className="me-2",
                                                    ),
                                                ],
                                                className="mb-2",
                                            ),
                                            html.Small(
                                                [
                                                    "Source: ",
                                                    html.A(
                                                        "U.S. Energy Information Administration",
                                                        href="https://www.eia.gov/electricity/data/state/emission_annual.xlsx",
                                                        target="_blank",
                                                        style={"color": "#003660"},
                                                    ),
                                                ],
                                                className="text-muted",
                                            ),
                                        ]
                                    )
                                ],
                                className="mb-3 border-start border-secondary border-1",
                            ),
                            # Dataset 3: Electricity Generation
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.H6(
                                                "Total Electricity Generation by State",
                                                className="card-title mb-2",
                                                style={"color": "#003660"},
                                            ),
                                            html.P(
                                                "This dataset provides a detailed view of electric power operations in the United States such as electricity generation, fuel consumption, fossil fuel stocks, and fuel receipts. The data is used to calculate upstream fuel input (coal, natural gas, etc.) quantities avoided by energy efficiency recommendations.",
                                                className="mb-2",
                                            ),
                                            html.Ul(
                                                [
                                                    html.Li("Fuel consumption data"),
                                                    html.Li(
                                                        "Fossil fuel stocks information"
                                                    ),
                                                    html.Li("Fuel receipts tracking"),
                                                ],
                                                className="mb-2",
                                            ),
                                            html.Div(
                                                [
                                                    dbc.Badge(
                                                        "Excel (.xlsx)",
                                                        color="light",
                                                        text_color="dark",
                                                        className="me-2",
                                                    ),
                                                    dbc.Badge(
                                                        "6.8 MB",
                                                        color="light",
                                                        text_color="dark",
                                                        className="me-2",
                                                    ),
                                                ],
                                                className="mb-2",
                                            ),
                                            html.Small(
                                                [
                                                    "Source: ",
                                                    html.A(
                                                        "U.S. Energy Information Administration",
                                                        href="https://www.eia.gov/electricity/data/state/annual_generation_state.xls",
                                                        target="_blank",
                                                        style={"color": "#003660"},
                                                    ),
                                                ],
                                                className="text-muted",
                                            ),
                                        ]
                                    )
                                ],
                                className="mb-3 border-start border-secondary border-1",
                            ),
                            # Dataset 4: Producer Price Index
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.H6(
                                                "Producer Price Index (PPI) Data",
                                                className="card-title mb-2",
                                                style={"color": "#003660"},
                                            ),
                                            html.P(
                                                "The dataset measures the average change over time in the selling prices received by domestic producers for their output. The dataset is used to adjust the investments and savings to present day values in order to determine their investment cost, energy cost, and payback periods.",
                                                className="mb-2",
                                            ),
                                            html.Div(
                                                [
                                                    dbc.Badge(
                                                        "Excel (.xlsx)",
                                                        color="light",
                                                        text_color="dark",
                                                        className="me-2",
                                                    )
                                                ],
                                                className="mb-2",
                                            ),
                                            html.Small(
                                                [
                                                    "Source: ",
                                                    html.A(
                                                        "Bureau of Labor Statistics",
                                                        href="https://www.bls.gov/data/",
                                                        target="_blank",
                                                        style={"color": "#003660"},
                                                    ),
                                                ],
                                                className="text-muted",
                                            ),
                                        ]
                                    )
                                ],
                                className="mb-3 border-start border-secondary border-1",
                            ),
                            # Dataset 5: Combustion Emission Factors (with collapsible table)
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        html.H6(
                                            "Combustion Emission Factors",
                                            className="mb-0",
                                            style={"color": "#003660"},
                                        )
                                    ),
                                    dbc.CardBody(
                                        [
                                            html.P(
                                                "The dataset is used to determine air pollutant emission quantities (CO₂, SOₓ, NOₓ, etc.) avoided by energy efficiency recommendations that lead to onsite fuel savings. Emission factors are compiled from EPA's AP-42 guidelines for stationary source emissions.",
                                                className="mb-2",
                                            ),
                                            html.Div(
                                                [
                                                    dbc.Badge(
                                                        "PDF",
                                                        color="light",
                                                        text_color="dark",
                                                        className="me-2",
                                                    )
                                                ],
                                                className="mb-2",
                                            ),
                                            html.Small(
                                                [
                                                    "Source: ",
                                                    html.A(
                                                        "EPA AP-42 Compilation",
                                                        href="https://www.epa.gov/air-emissions-factors-and-quantification/ap-42-compilation-air-emissions-factors-stationary-sources",
                                                        target="_blank",
                                                        style={"color": "#003660"},
                                                    ),
                                                ],
                                                className="text-muted mb-3",
                                            ),
                                            # Collapsible emissions factors table
                                            dbc.Button(
                                                [
                                                    html.I(
                                                        className="fas fa-chevron-right me-2"
                                                    ),
                                                    "View Emission Factors Table",
                                                ],
                                                id="collapse-button-emissions",
                                                className="mb-3 w-100 text-start",
                                                style={
                                                    "backgroundColor": "#DAE6E6",
                                                    "borderColor": "#003660",
                                                    "color": "#003660",
                                                },
                                                size="sm",
                                            ),
                                            dbc.Collapse(
                                                dbc.Table(
                                                    [
                                                        html.Thead(
                                                            [
                                                                html.Tr(
                                                                    [
                                                                        html.Th(
                                                                            "IAC Energy Source Type"
                                                                        ),
                                                                        html.Th(
                                                                            "IAC Fuel Code ID"
                                                                        ),
                                                                        html.Th(
                                                                            "Description"
                                                                        ),
                                                                        html.Th(
                                                                            "CO₂ (kg/MMBtu)"
                                                                        ),
                                                                        html.Th(
                                                                            "SO₂ (kg/MMBtu)"
                                                                        ),
                                                                        html.Th(
                                                                            "NOₓ (kg/MMBtu)"
                                                                        ),
                                                                    ]
                                                                )
                                                            ]
                                                        ),
                                                        html.Tbody(
                                                            [
                                                                html.Tr(
                                                                    [
                                                                        html.Td(
                                                                            "Natural Gas"
                                                                        ),
                                                                        html.Td("E2"),
                                                                        html.Td(
                                                                            "Natural gas combustion"
                                                                        ),
                                                                        html.Td(
                                                                            "53.06"
                                                                        ),
                                                                        html.Td(
                                                                            "0.00026682"
                                                                        ),
                                                                        html.Td(
                                                                            "0.078933902"
                                                                        ),
                                                                    ]
                                                                ),
                                                                html.Tr(
                                                                    [
                                                                        html.Td(
                                                                            "L.P.G"
                                                                        ),
                                                                        html.Td("E3"),
                                                                        html.Td(
                                                                            "Liquified petroleum gas combustion"
                                                                        ),
                                                                        html.Td(
                                                                            "61.71"
                                                                        ),
                                                                        html.Td(
                                                                            "0.00671968"
                                                                        ),
                                                                        html.Td(
                                                                            "0.066085045"
                                                                        ),
                                                                    ]
                                                                ),
                                                                html.Tr(
                                                                    [
                                                                        html.Td(
                                                                            "#1 Fuel Oil"
                                                                        ),
                                                                        html.Td("E4"),
                                                                        html.Td(
                                                                            "Fuel Oil Combustion"
                                                                        ),
                                                                        html.Td("75.2"),
                                                                        html.Td(
                                                                            "0.07821222"
                                                                        ),
                                                                        html.Td(
                                                                            "0.055079029"
                                                                        ),
                                                                    ]
                                                                ),
                                                                html.Tr(
                                                                    [
                                                                        html.Td(
                                                                            "#2 Fuel Oil"
                                                                        ),
                                                                        html.Td("E5"),
                                                                        html.Td(
                                                                            "Fuel Oil Combustion"
                                                                        ),
                                                                        html.Td(
                                                                            "73.96"
                                                                        ),
                                                                        html.Td(
                                                                            "0.02300359"
                                                                        ),
                                                                        html.Td(
                                                                            "0.055079029"
                                                                        ),
                                                                    ]
                                                                ),
                                                                html.Tr(
                                                                    [
                                                                        html.Td(
                                                                            "#4 Fuel Oil"
                                                                        ),
                                                                        html.Td("E6"),
                                                                        html.Td(
                                                                            "Average"
                                                                        ),
                                                                        html.Td(
                                                                            "74.75"
                                                                        ),
                                                                        html.Td(
                                                                            "0.28422219"
                                                                        ),
                                                                        html.Td(
                                                                            "0.073258708"
                                                                        ),
                                                                    ]
                                                                ),
                                                                html.Tr(
                                                                    [
                                                                        html.Td(
                                                                            "#6 Fuel Oil"
                                                                        ),
                                                                        html.Td("E7"),
                                                                        html.Td(
                                                                            "Fuel Oil combustion"
                                                                        ),
                                                                        html.Td("75.1"),
                                                                        html.Td(
                                                                            "0.75145075"
                                                                        ),
                                                                        html.Td(
                                                                            "0.109618067"
                                                                        ),
                                                                    ]
                                                                ),
                                                                html.Tr(
                                                                    [
                                                                        html.Td("Coal"),
                                                                        html.Td("E8"),
                                                                        html.Td(
                                                                            "Bituminous and subbituminous coal combustion"
                                                                        ),
                                                                        html.Td(
                                                                            "94.67"
                                                                        ),
                                                                        html.Td(
                                                                            "0.78328289"
                                                                        ),
                                                                        html.Td(
                                                                            "0.109557215"
                                                                        ),
                                                                    ]
                                                                ),
                                                                html.Tr(
                                                                    [
                                                                        html.Td("Wood"),
                                                                        html.Td("E9"),
                                                                        html.Td(
                                                                            "Wood residue combustion in boilers"
                                                                        ),
                                                                        html.Td("93.8"),
                                                                        html.Td(
                                                                            "0.20571066"
                                                                        ),
                                                                        html.Td(
                                                                            "0.140589569"
                                                                        ),
                                                                    ]
                                                                ),
                                                                html.Tr(
                                                                    [
                                                                        html.Td(
                                                                            "Paper"
                                                                        ),
                                                                        html.Td("E10"),
                                                                        html.Td(
                                                                            "Same as Wood"
                                                                        ),
                                                                        html.Td("93.8"),
                                                                        html.Td(
                                                                            "0.20571066"
                                                                        ),
                                                                        html.Td(
                                                                            "0.140589569"
                                                                        ),
                                                                    ]
                                                                ),
                                                                html.Tr(
                                                                    [
                                                                        html.Td(
                                                                            "Other Gas"
                                                                        ),
                                                                        html.Td("E11"),
                                                                        html.Td(
                                                                            "Same as LPG"
                                                                        ),
                                                                        html.Td(
                                                                            "66.72"
                                                                        ),
                                                                        html.Td(
                                                                            "0.00671968"
                                                                        ),
                                                                        html.Td(
                                                                            "0.066085045"
                                                                        ),
                                                                    ]
                                                                ),
                                                                html.Tr(
                                                                    [
                                                                        html.Td(
                                                                            "Other Energy"
                                                                        ),
                                                                        html.Td("E12"),
                                                                        html.Td(
                                                                            "Average of all emission factor values"
                                                                        ),
                                                                        html.Td(
                                                                            "76.28"
                                                                        ),
                                                                        html.Td(
                                                                            "0.23452991"
                                                                        ),
                                                                        html.Td(
                                                                            "0.089487518"
                                                                        ),
                                                                    ]
                                                                ),
                                                            ]
                                                        ),
                                                    ],
                                                    bordered=True,
                                                    hover=True,
                                                    responsive=True,
                                                    striped=True,
                                                ),
                                                id="collapse-emissions",
                                                is_open=False,
                                            ),
                                        ]
                                    ),
                                ],
                                className="shadow-sm mb-3 border-start border-secondary border-1",
                            ),
                            # Dataset 6: NAICS Codes
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.H6(
                                                "North American Industry Classification System Codes",
                                                className="card-title mb-2",
                                                style={"color": "#003660"},
                                            ),
                                            html.P(
                                                "Standardized industry classification codes used to categorize facilities and recommendations by industry type. NAICS codes enable consistent analysis across different industrial sectors and facilitate comparison of energy efficiency measures within similar industries.",
                                                className="mb-2",
                                            ),
                                            html.Div(
                                                [
                                                    dbc.Badge(
                                                        "Excel (.xlsx)",
                                                        color="light",
                                                        text_color="dark",
                                                        className="me-2",
                                                    ),
                                                    dbc.Badge(
                                                        "340 KB",
                                                        color="light",
                                                        text_color="dark",
                                                        className="me-2",
                                                    ),
                                                ],
                                                className="mb-2",
                                            ),
                                            html.Small(
                                                [
                                                    "Source: ",
                                                    html.A(
                                                        "NAICS Association",
                                                        href="https://www.naics.com/search/",
                                                        target="_blank",
                                                        style={"color": "#003660"},
                                                    ),
                                                ],
                                                className="text-muted",
                                            ),
                                        ]
                                    )
                                ],
                                className="mb-3 border-start border-secondary border-1",
                            ),
                            # Dataset 7: SIC Codes
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.H6(
                                                "Standard Industrial Classification System Codes",
                                                className="card-title mb-2",
                                                style={"color": "#003660"},
                                            ),
                                            html.P(
                                                "Legacy industry classification system with crosswalk mapping to NAICS codes. SIC codes are used to maintain consistency with historical data and provide backward compatibility for older assessment records in the database.",
                                                className="mb-2",
                                            ),
                                            html.Div(
                                                [
                                                    dbc.Badge(
                                                        "Excel (.xlsx)",
                                                        color="light",
                                                        text_color="dark",
                                                        className="me-2",
                                                    ),
                                                    dbc.Badge(
                                                        "149 KB",
                                                        color="light",
                                                        text_color="dark",
                                                        className="me-2",
                                                    ),
                                                ],
                                                className="mb-2",
                                            ),
                                            html.Small(
                                                [
                                                    "Source: ",
                                                    html.A(
                                                        "NAICS Association",
                                                        href="https://www.naics.com/search/",
                                                        target="_blank",
                                                        style={"color": "#003660"},
                                                    ),
                                                ],
                                                className="text-muted",
                                            ),
                                        ]
                                    )
                                ],
                                className="mb-3 border-start border-secondary border-1",
                            ),
                            # Dataset 8: Assessment Recommendation Codes
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.H6(
                                                "Assessment Recommendation Codes",
                                                className="card-title mb-2",
                                                style={"color": "#003660"},
                                            ),
                                            html.P(
                                                "Standardized hierarchical coding system for categorizing energy efficiency recommendations by technology type, application area, and specific implementation details. These codes enable systematic analysis and comparison of different energy efficiency measures across facilities.",
                                                className="mb-2",
                                            ),
                                            html.Div(
                                                [
                                                    dbc.Badge(
                                                        "PDF",
                                                        color="light",
                                                        text_color="dark",
                                                        className="me-2",
                                                    )
                                                ],
                                                className="mb-2",
                                            ),
                                            html.Small(
                                                [
                                                    "Source: ",
                                                    html.A(
                                                        "IAC ARC Manual",
                                                        href="https://iac.university/technicalDocs/ARC_list_9.1.pdf",
                                                        target="_blank",
                                                        style={"color": "#003660"},
                                                    ),
                                                ],
                                                className="text-muted",
                                            ),
                                        ]
                                    )
                                ],
                                className="mb-4 border-start border-secondary border-1",
                            ),
                        ],
                        width=10,
                        className="px-5",  # Add same margins as rest of page
                    )
                ],
                justify="center",
            ),
        ],
        className="container-fluid px-5 py-3",  # Increased margins for narrower content
    )
    return create_base_layout(content)
