import plotly.express as px

def create_boxplot_cost_chart(boxplot_cost_df):
    return px.box(boxplot_cost_df, 
                  x="impstatus", 
                  y="ref_year_impcost", 
                  points="all")