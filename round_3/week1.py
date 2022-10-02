import plotly.express as px
import plotly.graph_objects as go


def get_fig_q1(df):
    return px.bar(x=[1, 2, 3, 4, 5], y=[2, 3, 4, 2, 3])
