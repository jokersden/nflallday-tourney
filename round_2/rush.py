import plotly.express as px
import plotly.graph_objects as go


def get_toprushes(df):
    df = (
        df.groupby("video_url")
        .agg({"TOTAL": "sum", "PLAYER": "min"})
        .reset_index()
        .nlargest(5, "TOTAL")
    )
    return (df["video_url"].values, df["PLAYER"].values, df["TOTAL"].values)


def get_rush_formation(df):
    df = df.groupby(["PLAYER", "offense_formation"]).sum().reset_index()
    # df = df.sort_values(by=["offense_formation", "PLAYER"])
    fig = px.bar(
        df,
        x="PLAYER",
        y="TOTAL",
        color="offense_formation",
        color_discrete_sequence=px.colors.sequential.Agsunset,
        labels=dict(
            offense_formation="Offence Formation",
            PLAYER="Player Name",
            TOTAL="Sales Volume $",
        ),
        title="Player, sales and Offense formation",
    )
    fig.update_xaxes(tickangle=45, showspikes=False)
    fig.update_layout(
        hovermode="x unified",
        legend=dict(yanchor="top", y=1, x=0, orientation="h"),
    )
    return fig


def get_rush_td_player(df):
    col = "rush_touchdown_enc"
    fig = px.bar(
        df.groupby(["PLAYER", col]).sum().reset_index(),
        x="PLAYER",
        y="TOTAL",
        color=col,
        custom_data=["rush_touchdown_enc"],
        labels=dict(
            rush_touchdown_enc="", PLAYER="Player Name", TOTAL="Sales Volume($)"
        ),
        color_discrete_sequence=["green", "red"],
    )
    fig.update_traces(
        hovertemplate="<br> <b>%{x}</b><br><br>"
        + "Rushing Yards: %{x} </br>"
        + "TD?: %{customdata[0]} </br>"
        + "Volume Sold: $%{y:,.2f} </br>"
        + "Average Price: $%{customdata[0]:,.2f} <extra></extra>"
    )
    fig.update_layout(
        hovermode="x unified",
        legend=dict(yanchor="top", xanchor="right", y=1, x=1, orientation="h"),
    )
    fig.update_xaxes(showspikes=False)
    return fig


def get_rush_td_tot(df):
    col = "rush_touchdown_enc"
    fig = px.scatter(
        df.groupby(["rushing_yards", col])
        .agg({"AVG_PRICE": "mean", "TOTAL": "sum", "PLAYER": "min"})
        .reset_index(),
        x="rushing_yards",
        y="TOTAL",
        color=col,
        size="AVG_PRICE",
        custom_data=["AVG_PRICE", "PLAYER", "rush_touchdown_enc"],
        labels=dict(
            rush_touchdown_enc="",
            rushing_yards="Rushing Yards",
            TOTAL="Sales Volume($)",
        ),
        title="Do Rushing Yards and converting to a TD has an effect on sales?",
    )
    fig.update_traces(
        hovertemplate="<br> <b>%{customdata[1]}</b><br><br>"
        + "Rushing Yards: %{x} </br>"
        + "Was it a TD: %{customdata[2]} </br>"
        + "Volume Sold: $%{y:,.2f} </br>"
        + "Average Price: $%{customdata[0]:,.2f} <extra></extra>"
    )
    fig.update_layout(
        hovermode="x unified",
        legend=dict(yanchor="top", xanchor="right", y=1, x=1, orientation="h"),
    )
    fig.update_xaxes(showspikes=False)
    return fig
