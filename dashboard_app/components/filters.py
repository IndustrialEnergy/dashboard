from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from pathlib import Path


def get_naics_descriptions():
    """
    Load NAICS descriptions from the hierarchy CSV file.
    Returns a dictionary mapping 3-digit NAICS prefixes to descriptions.
    """
    try:
        # Get the path to the NAICS hierarchy file
        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent.parent
        naics_file = project_root / "data" / "processed" / "naics_hierarchy.csv"

        if naics_file.exists():
            # Read the NAICS hierarchy file
            naics_df = pd.read_csv(naics_file, dtype={"naics_code": str})

            # Create a mapping of 3-digit prefixes to descriptions
            naics_descriptions = {}
            for _, row in naics_df.iterrows():
                naics_code = str(row["naics_code"]).strip()
                industry_description = row["industry_description"].strip()
                naics_descriptions[naics_code] = industry_description

            return naics_descriptions
        else:
            print(
                f"NAICS hierarchy file not found at {naics_file}, using fallback descriptions"
            )
            return {}
    except Exception as e:
        print(f"Error loading NAICS descriptions: {e}, using fallback descriptions")
        return {}


def get_wildcard_patterns(codes, code_type="arc", df=None):
    """
    Generate wildcard patterns based on common prefixes in the codes.

    Args:
        codes: List of unique codes
        code_type: "arc" or "naics" to determine pattern generation
        df: DataFrame containing hierarchy data (for ARC patterns)

    Returns:
        List of dictionaries with wildcard options
    """
    wildcard_options = []

    if code_type == "arc" and df is not None:
        # Use actual ARC hierarchy data from the dataset

        # Get main categories (e.g., 2.1*, 2.2*, 2.3*, 2.4*)
        main_categories = (
            df[["main_code", "main_description"]].dropna().drop_duplicates()
        )
        for _, row in main_categories.iterrows():
            main_code = str(row["main_code"])
            main_desc = row["main_description"]
            # Check if any codes start with this main category
            if any(str(code).startswith(main_code) for code in codes):
                wildcard_options.append(
                    {
                        "label": f"{main_code}* - {main_desc}",
                        "value": f"{main_code}*",
                    }
                )

        # Get sub categories (e.g., 2.11*, 2.12*, 2.21*, 2.41*)
        sub_categories = df[["sub_code", "sub_description"]].dropna().drop_duplicates()
        for _, row in sub_categories.iterrows():
            sub_code = str(row["sub_code"])
            sub_desc = row["sub_description"]
            # Check if any codes start with this sub category
            if any(str(code).startswith(sub_code) for code in codes):
                wildcard_options.append(
                    {
                        "label": f"{sub_code}* - {sub_desc}",
                        "value": f"{sub_code}*",
                    }
                )

        # Sort by value to have a logical order (main categories first, then sub)
        wildcard_options.sort(key=lambda x: (len(x["value"]), x["value"]))

    elif code_type == "naics":
        # NAICS codes - generate patterns for 3-digit industry groups
        prefixes = {}
        for code in codes:
            code_str = str(code)
            if len(code_str) >= 3:
                prefix = code_str[:3]
                if prefix not in prefixes:
                    prefixes[prefix] = 0
                prefixes[prefix] += 1

        # Get NAICS descriptions from CSV file
        naics_descriptions = get_naics_descriptions()

        # Fallback descriptions for common manufacturing codes if CSV loading fails
        fallback_descriptions = {
            "311": "Food Manufacturing",
            "312": "Beverage and Tobacco Product Manufacturing",
            "313": "Textile Mills",
            "314": "Textile Product Mills",
            "315": "Apparel Manufacturing",
            "316": "Leather and Allied Product Manufacturing",
            "321": "Wood Product Manufacturing",
            "322": "Paper Manufacturing",
            "323": "Printing and Related Support Activities",
            "324": "Petroleum and Coal Products Manufacturing",
            "325": "Chemical Manufacturing",
            "326": "Plastics and Rubber Products Manufacturing",
            "327": "Nonmetallic Mineral Product Manufacturing",
            "331": "Primary Metal Manufacturing",
            "332": "Fabricated Metal Product Manufacturing",
            "333": "Machinery Manufacturing",
            "334": "Computer and Electronic Product Manufacturing",
            "335": "Electrical Equipment Manufacturing",
            "336": "Transportation Equipment Manufacturing",
            "337": "Furniture and Related Product Manufacturing",
            "339": "Miscellaneous Manufacturing",
        }

        # Use loaded descriptions, fallback to hardcoded if needed
        descriptions_to_use = (
            naics_descriptions if naics_descriptions else fallback_descriptions
        )

        for prefix, count in prefixes.items():
            if (
                count >= 2
            ):  # Only include if there are at least 2 codes with this prefix
                description = descriptions_to_use.get(
                    prefix, f"Industry Group {prefix}"
                )
                wildcard_options.append(
                    {
                        "label": f"{prefix}* - {description}",  # Show code prefix with description
                        "value": f"{prefix}*",  # Internal wildcard pattern
                    }
                )

    return wildcard_options


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
                    # sector-description filter with wildcards
                    dbc.Col(
                        [
                            html.Label("Sector:", className="filter-label"),
                            dcc.Dropdown(
                                id="sector-filter",
                                options=naics_wildcards
                                + [
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
                                placeholder="Select Sector (use * patterns for groups)",
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
                    # ARC filter with wildcards
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
                                placeholder="Select Recommendation (use * patterns for groups)",
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


def apply_wildcard_filter(df, filter_values, column_name):
    """
    Apply wildcard filtering to a dataframe.

    Args:
        df: DataFrame to filter
        filter_values: List of filter values (can include wildcards like "2.4*" or "311*")
        column_name: Column name to filter on

    Returns:
        Filtered DataFrame
    """
    if not filter_values:
        return df

    # Separate wildcard patterns from exact matches
    exact_matches = []
    wildcard_patterns = []

    for value in filter_values:
        if str(value).endswith("*"):
            wildcard_patterns.append(str(value)[:-1])  # Remove the *
        else:
            exact_matches.append(value)

    # Create filter mask
    mask = pd.Series(False, index=df.index)

    # Apply exact matches
    if exact_matches:
        mask |= df[column_name].isin(exact_matches)

    # Apply wildcard patterns
    for pattern in wildcard_patterns:
        mask |= df[column_name].astype(str).str.startswith(pattern)

    return df[mask]
