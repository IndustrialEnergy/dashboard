import plotly.express as px

def create_boxplot_payback_chart(boxplot_cost_df):
    return px.box(boxplot_cost_df, 
                  x="impstatus", 
                  y="payback", 
                  points="all")