def filter_outliers(df, column_name, std_threshold=2):
    if df.empty or column_name not in df.columns:
        return df
    mean = df[column_name].mean()
    std = df[column_name].std()
    return df[
        (df[column_name] >= mean - std_threshold * std)
        & (df[column_name] <= mean + std_threshold * std)
    ]
