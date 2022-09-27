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


def get_rush_tot_player(df, col_name, col):
    df["label"] = col
    fig = px.bar(
        df.groupby(["PLAYER", col_name])
        .agg({"TOTAL": "sum", "AVG_PRICE": "max", "label": "min"})
        .reset_index(),
        x="PLAYER",
        y="TOTAL",
        color=col_name,
        custom_data=[col_name, "AVG_PRICE", "label"],
        labels=dict(
            rush_touchdown_enc="",
            PLAYER="Player Name",
            TOTAL="Sales Volume($)",
            winning="",
        ),
        color_discrete_sequence=["mediumseagreen", "palevioletred"],
        title="Rush ended up in a TD has any effect on sales?",
    )
    fig.update_traces(
        hovertemplate="<br> <b>%{x}</b><br><br>"
        + "Moment Price: $%{customdata[1]:,.2f} <br>"
        + "%{customdata[2]} : %{customdata[0]} <br>"
        + "Volume Sold: $%{y:,.2f} <extra></extra>"
    )
    fig.update_layout(
        hovermode="x unified",
        legend=dict(yanchor="top", xanchor="right", y=1.1, x=1, orientation="h"),
    )
    fig.update_xaxes(showspikes=False, tickangle=45)
    return fig


def get_rush_avg_player(df, col_name, col):
    df["label"] = col
    fig = px.bar(
        df.groupby(["PLAYER", col_name])
        .agg({"TOTAL": "sum", "AVG_PRICE": "max", "label": "min"})
        .reset_index(),
        x="PLAYER",
        y="AVG_PRICE",
        color=col_name,
        custom_data=[col_name, "TOTAL", "label"],
        labels=dict(
            rush_touchdown_enc="",
            PLAYER="Player Name",
            AVG_PRICE="Moment Price($)",
            winning="",
        ),
        barmode="group",
        color_discrete_sequence=["mediumseagreen", "palevioletred"],
        title="Rush ended up in a TD has any effect on sales?",
    )
    fig.update_traces(
        hovertemplate="<br> <b>%{x}</b><br><br>"
        + "Moment Price: $%{y:,.2f} <br>"
        + "%{customdata[2]} : %{customdata[0]} <br>"
        + "Volume Sold: $%{customdata[1]:,.2f} <extra></extra>"
    )
    fig.update_layout(
        hovermode="x unified",
        legend=dict(yanchor="top", xanchor="right", y=1.1, x=1, orientation="h"),
    )
    fig.update_xaxes(showspikes=False, tickangle=45)
    return fig


def get_rush_td_tot(df):
    col = "rush_touchdown_enc"
    fig = px.scatter(
        df.groupby(["rushing_yards", col])
        .agg({"AVG_PRICE": "max", "TOTAL": "sum"})
        .reset_index(),
        x="rushing_yards",
        y="TOTAL",
        color=col,
        size="AVG_PRICE",
        custom_data=["AVG_PRICE", "rush_touchdown_enc"],
        labels=dict(
            rush_touchdown_enc="",
            rushing_yards="Rushing Yards",
            TOTAL="Sales Volume($)",
        ),
        title="Do Rushing Yards and converting to a TD has an effect on price of the moment?",
    )
    fig.update_traces(
        hovertemplate="<br> <b>%{customdata[1]}</b><br><br>"
        + "Rushing Yards: %{x} </br>"
        + "Was it a TD: %{customdata[2]} </br>"
        + "Volume Sold: $%{y:,.2f} </br>"
        + "Moment Price: $%{customdata[0]:,.2f} <extra></extra>"
    )
    fig.update_layout(
        hovermode="x unified",
        legend=dict(yanchor="top", xanchor="right", y=1, x=1, orientation="h"),
        coloraxis_colorbar={"title": "Rushing Yards"},
        legend_title="Rushing Yards",
    )
    fig.update_xaxes(showspikes=False)
    return fig


def get_win_total_box(df):
    fig = px.box(
        df,
        y="TOTAL",
        x="rush_touchdown_enc",
        color="winning",
        color_discrete_sequence=["lightseagreen", "mediumvioletred"],
        labels=dict(
            rush_touchdown_enc="Touchdown status", TOTAL="Sales volume($)", winning=""
        ),
        title="Touchdown and victories' impact on sales volume",
        custom_data=["PLAYER", "AVG_PRICE"],
    )
    fig.update_traces(
        hovertemplate="<br> <b>%{customdata[0]}</b><br><br>"
        + "Rushing Yards: %{x} </br>"
        + "Volume Sold: $%{y:,.2f} </br>"
        + "Moment Price: $%{customdata[1]:,.2f} <extra></extra>"
    )
    fig.update_layout(
        hovermode="x unified",
        legend=dict(yanchor="top", xanchor="right", y=1.1, x=1, orientation="h"),
    )
    fig.update_xaxes(showspikes=False)
    return fig


def get_win_avg_box(df):
    fig = px.box(
        df,
        y="AVG_PRICE",
        x="rush_touchdown_enc",
        color="winning",
        color_discrete_sequence=["lightseagreen", "mediumvioletred"],
        labels=dict(
            rush_touchdown_enc="Touchdown status",
            AVG_PRICE="Moment price($)",
            winning="",
        ),
        title="Touchdown and victories' impact on price of the moment",
        custom_data=["PLAYER", "TOTAL"],
    )
    fig.update_traces(
        hovertemplate="<br> <b>%{customdata[0]}</b><br><br>"
        + "Rushing Yards: %{x} </br>"
        + "Volume Sold: $%{customdata[1]:,.2f} </br>"
        + "Moment Price: $%{y:,.2f} <extra></extra>"
    )
    fig.update_layout(
        hovermode="x unified",
        legend=dict(yanchor="top", xanchor="right", y=1.1, x=1, orientation="h"),
    )
    fig.update_xaxes(showspikes=False)
    return fig
