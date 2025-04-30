import plotly.express as px


def create_boxplot_payback_chart(boxplot_cost_df):
    # sample the data if it's too large
    if len(boxplot_cost_df) > 10000:
        boxplot_cost_df = boxplot_cost_df.sample(n=10000, random_state=42)

    # define status labels mapping
    status_labels = {
        "I": "Implemented",
        "N": "Not Implemented",
        "P": "Pending",
        "K": "Unknown",
    }

    fig = px.box(
        boxplot_cost_df,
        x="arc2",
        y="payback",
        color="impstatus",
        boxmode="group",
        labels={
            "arc2": "Recommendation Type",
            "payback": "Payback Period (years)",
            "impstatus": "Implementation Status",
        },
        category_orders={"impstatus": ["I", "N", "P", "K"]},
    )

    # update legend labels
    fig.for_each_trace(lambda t: t.update(name=status_labels[t.name]))

    # update legend layout
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        )
    )

    return fig
