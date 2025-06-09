from dashboard_app.helpers.get_naics_descriptions import get_naics_descriptions


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

        # Use a dictionary to store unique patterns and avoid duplicates
        unique_patterns = {}

        # Get main categories (e.g., 2.1*, 2.2*, 2.3*, 2.4*)
        main_categories = (
            df[["main_code", "main_description"]].dropna().drop_duplicates()
        )
        for _, row in main_categories.iterrows():
            main_code = str(row["main_code"])
            main_desc = row["main_description"]
            # Check if any codes start with this main category
            if any(str(code).startswith(main_code) for code in codes):
                pattern_key = f"{main_code}*"
                unique_patterns[pattern_key] = f"{main_code}* - {main_desc}"

        # Get sub categories (e.g., 2.11*, 2.12*, 2.21*, 2.41*)
        sub_categories = df[["sub_code", "sub_description"]].dropna().drop_duplicates()
        for _, row in sub_categories.iterrows():
            sub_code = str(row["sub_code"])
            sub_desc = row["sub_description"]
            # Check if any codes start with this sub category
            if any(str(code).startswith(sub_code) for code in codes):
                pattern_key = f"{sub_code}*"
                # Only add if not already present (main categories take precedence)
                if pattern_key not in unique_patterns:
                    unique_patterns[pattern_key] = f"{sub_code}* - {sub_desc}"

        # Convert to wildcard options format
        for pattern_value, pattern_label in unique_patterns.items():
            wildcard_options.append(
                {
                    "label": pattern_label,
                    "value": pattern_value,
                }
            )

        # Sort by value to have a logical order (main categories first, then sub)
        wildcard_options.sort(key=lambda x: (len(x["value"]), x["value"]))

    elif code_type == "naics":
        # NAICS codes - generate patterns for multiple hierarchy levels
        patterns = {}

        for code in codes:
            code_str = str(code)
            # Generate patterns for different lengths (2, 3, 4 digits)
            for length in [2, 3, 4]:
                if len(code_str) >= length:
                    prefix = code_str[:length]
                    if prefix not in patterns:
                        patterns[prefix] = 0
                    patterns[prefix] += 1

        # Get NAICS descriptions from CSV file
        naics_descriptions = get_naics_descriptions()

        # Create wildcard options organized by hierarchy level
        # Process in order: 2-digit (Sectors), 3-digit (Subsectors), 4-digit (Industry Groups)
        for length in [2, 3, 4]:
            level_patterns = []
            for prefix, count in patterns.items():
                if (
                    len(prefix) == length and count >= 2
                ):  # Only include if there are at least 2 codes with this prefix
                    description_data = naics_descriptions.get(
                        prefix, {"description": f"Code {prefix}", "level": "Unknown"}
                    )
                    description = description_data["description"]

                    level_patterns.append(
                        {"label": f"{prefix}* - {description}", "value": f"{prefix}*"}
                    )

            # Sort patterns within each level by prefix
            level_patterns.sort(key=lambda x: x["value"])
            wildcard_options.extend(level_patterns)

    return wildcard_options
