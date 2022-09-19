import plotly.express as px
import plotly.graph_objects as go

cats = ["rushing_yards", "passing_yards", "completions", "attempts", "receiving_yards"]
cat_names = [
    "Rushing Yards",
    "Passing Yards",
    "Completions",
    "Attempts",
    "Receiving Yards",
]


def get_fig_player_total(df, week):
    df_top20 = (
        df.groupby("player")
        .agg(
            total=("price", "sum"),
            avg_price=("price", "mean"),
            sales=("sales", "count"),
        )
        .reset_index()
        .nlargest(30, "total")
    )
    fig_player_total = px.bar(
        df_top20,
        x="player",
        y="total",
        color="avg_price",
        hover_name="player",
        text=df_top20.avg_price,
        text_auto=True,
        color_continuous_scale=px.colors.sequential.Mint_r,
        title=f"Which Players were fan favorites in {week}",
        labels=dict(player="Player", total="Amount (USD)", avg_price="Average Price"),
    )
    df_top20["adj"] = df_top20.sales * (max(df_top20.total) / max(df_top20.sales)) * 0.8

    fig_player_total.update_traces(
        hovertemplate="<br> <b>%{x}</b><br><br>"
        + "Volume Sold: $%{y:,.2f} </br>"
        + "Average Price: $%{text:,.2f} <extra></extra>"
    )
    fig_player_total.add_trace(
        go.Scatter(
            x=df_top20.player,
            y=df_top20.adj,
            name="Number of sales",
            meta=df_top20.sales,
            hovertemplate="<br>Number of sales: %{meta} </br><extra></extra>",
        )
    )
    fig_player_total.update_xaxes(tickangle=35, showspikes=False)
    fig_player_total.update_yaxes(showspikes=False)
    fig_player_total.update_layout(
        hovermode="x unified",
        legend=dict(yanchor="top", y=1, x=0),
    )
    return fig_player_total


def get_fig_playaer_stats(df, col, col_name, week="1"):
    df.fantasy_points_ppr = df.apply(lambda x: round(x.fantasy_points_ppr, 2), axis=1)
    labels = {
        "player_name": "Player Name",
        "team_x": "Team",
        "fantasy_points_ppr": "Fantasy Points",
    }
    labels[col] = col_name
    fig_player_stats = px.bar(
        df.groupby("player").last().sort_values(by=col, ascending=False).head(20),
        x="player_name",
        y=col,
        color="fantasy_points_ppr",
        text="team_y",
        color_continuous_scale=px.colors.sequential.Teal,
        labels=labels,
        title=f"Top 20 players with highest {col_name} so far in this season.",
    )
    fig_player_stats.update_xaxes(tickangle=35, showspikes=False)
    fig_player_stats.update_layout(hovermode="x unified")
    return fig_player_stats


def get_top5_players(df):
    temp = (
        df.groupby("player")
        .agg(
            total=("price", "sum"),
            avg_price=("price", "mean"),
            sales=("sales", "count"),
            fantasy_points=("fantasy_points_ppr", "last"),
            headshot_url=("headshot_url", "last"),
            team=("team_x", "last"),
        )
        .reset_index()
        .nlargest(5, "total")
    )
    df_temp = df.groupby("player").last().reset_index()[cats + ["player"]]
    for i in cats:
        df_temp[i] = df_temp[i].rank(pct=True)
    radars = []
    for p in temp.player.values:
        data = df_temp[df_temp.player == p]
        figure = px.bar_polar(
            theta=cat_names,
            r=(data[cats].values[0]),  # line_close=True,
            hover_name=cat_names,
            color=cats,
            barnorm="fraction",
            labels=dict(r="Percentile"),
            range_r=[0, 1],
        )
        # figure.update_traces(fill="toself")
        figure.update_layout(hovermode="x unified", showlegend=False)
        figure.update_traces(
            hovertemplate="<br> <b>%{theta}</b><br><br>"
            + "Percentile: %{r:,.2f} </br><extra></extra>"
        )
        radars.append(figure)
    return temp, radars
