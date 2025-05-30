# import plotly.express as px
# import plotly.graph_objects as go
# import traceback
# import pandas as pd

# def create_boxplot_co2_chart(boxplot_co2_df):
#     return px.box(boxplot_co2_df,
#                   x="impstatus",
#                   y="emissions_avoided",
#                   color="impstatus",
#                   points="all")

import plotly.express as px
import plotly.graph_objects as go
import traceback
import pandas as pd
import plotly.io as pio


def create_boxplot_co2_chart(boxplot_co2_df):
    # sample the data if it's too large
    if len(boxplot_co2_df) > 10000:
        boxplot_co2_df = boxplot_co2_df.sample(n=10000, random_state=42)

    # define status labels mapping
    status_labels = {
        "I": "Implemented",
        "N": "Not Implemented",
        "P": "Pending",
        "K": "Unknown",
    }

    # check if dataframe is empty after filtering
    if boxplot_co2_df.empty:
        return px.scatter(title="No data available for the selected filters")

    fig = px.box(
        boxplot_co2_df,
        x="arc2",
        y="emissions_avoided",
        color="impstatus",
        boxmode="group",
        points="all",
        labels={
            "arc2": "Recommendation Type",
            "emissions_avoided": "CO2 Emissions Avoided (kg per year)",
            "impstatus": "Status",
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
