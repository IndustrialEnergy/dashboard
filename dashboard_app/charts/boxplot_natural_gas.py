import plotly.express as px
import plotly.graph_objects as go
import traceback
import pandas as pd


def create_boxplot_natural_gas_chart(boxplot_natural_gas_df):
    # sample the data if it's too large
    if len(boxplot_natural_gas_df) > 10000:
        boxplot_natural_gas_df = boxplot_natural_gas_df.sample(n=10000, random_state=42)

    # define status labels mapping
    status_labels = {
        "I": "Implemented",
        "N": "Not Implemented",
        "P": "Pending",
        "K": "Unknown",
    }

    # check if dataframe is empty after filtering
    if boxplot_natural_gas_df.empty:
        return px.scatter(title="No data available for the selected filters")

    fig = px.box(
        boxplot_natural_gas_df,
        x="arc2",
        y="conserved",
        color="impstatus",
        boxmode="group",
        points="suspectedoutliers",
        labels={
            "arc2": "Recommendation Type",
            "conserved": "Natural gas saved (MMBtu per year)",
            "impstatus": "Status",
        },
        category_orders={"impstatus": ["I", "N", "P", "K"]},
        template="plotly_white",
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