import plotly.express as px


def create_boxplot_payback_chart(boxplot_payback_df):
    # sample the data if it's too large
    if len(boxplot_payback_df) > 10000:
        boxplot_payback_df = boxplot_payback_df.sample(n=10000, random_state=42)

    # define status labels mapping
    status_labels = {
        "I": "Implemented",
        "N": "Not Implemented",
        "P": "Pending",
        "K": "Unknown",
    }

    # check if dataframe is empty after filtering
    if boxplot_payback_df.empty:
        return px.scatter(title="No data available for the selected filters")

    fig = px.box(
        boxplot_payback_df,
        x="arc2",
        y="payback_imputed",
        color="impstatus",
        boxmode="group",
        points="all",
        labels={
            "arc2": "Recommendation Type",
            "payback_imputed": "Payback Period (years)",
            "impstatus": "Implementation Status",
        },
        category_orders={"impstatus": ["I", "N", "P", "K"]},
        template="plotly_white",
    )

    fig.update_traces(
        marker=dict(size=5),  # boxplot point size
    )
    # update legend labels
    fig.for_each_trace(lambda t: t.update(name=status_labels[t.name]))

    # update legend layout - styling now handled by CSS
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
        boxgap=0.5,  # gap between boxes in same group for better spacing
        boxgroupgap=0.6,  # gap between different groups
        autosize=True,  # Responsive sizing - height controlled by CSS
        margin=dict(l=60, r=40, t=60, b=60),  # Reduced margins for tighter fit
    )

    return fig
