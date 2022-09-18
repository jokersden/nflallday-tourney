import plotly.express as px
import plotly.graph_objects as go


def get_fig_moment_playtype(df, week):
    df_daily_sales_moment_playtype = (
        df.groupby(["play_type"])
        .agg(
            total=("price", "sum"),
            avg_price=("price", "mean"),
            sales=("sales", "count"),
        )
        .reset_index()
    )
    fig_moment_playtype = px.bar(
        df_daily_sales_moment_playtype,
        x="play_type",
        y="total",
        color="avg_price",
        text="avg_price",
        text_auto=True,
        custom_data=[df_daily_sales_moment_playtype.avg_price],
        color_continuous_scale=px.colors.sequential.Tealgrn_r,
        title=f"Which play types were most sought after in {week}",
        labels=dict(
            play_type="Play Type", total="Amount (USD)", avg_price="Average Price"
        ),
    )
    fig_moment_playtype.update_traces(
        hovertemplate="<br> <b>%{x}</b><br><br>"
        + "Volume Sold: $%{y:,.2f} </br>"
        + "Average Price: $%{text:,.2f} <extra></extra>"
    )
    df_daily_sales_moment_playtype["adj"] = (
        df_daily_sales_moment_playtype.sales
        * (
            max(df_daily_sales_moment_playtype.total)
            / max(df_daily_sales_moment_playtype.sales)
        )
        * 0.8
    )
    fig_moment_playtype.add_trace(
        go.Scatter(
            x=df_daily_sales_moment_playtype.play_type,
            y=df_daily_sales_moment_playtype.adj,
            name="Number of sales",
            meta=df_daily_sales_moment_playtype.sales,
            hovertemplate="<br>Number of sales: %{meta} </br><extra></extra>",
        )
    )
    fig_moment_playtype.update_xaxes(tickangle=35)
    fig_moment_playtype.update_layout(
        hovermode="x unified", legend=dict(yanchor="top", y=1, x=0)
    )
    return fig_moment_playtype
