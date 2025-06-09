import pandas as pd


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
