import plotly.express as px


def get_fig_play_playtype(df, week="1"):
    fig_play_playtype = px.box(
        df,
        x="play_type",
        y="price",
        color="moment_tier",
        color_discrete_sequence=px.colors.sequential.Rainbow_r,
        labels=dict(play_type="Play Type", price="Amount (USD)", moment_tier="Tier"),
        title=f"Which tiers and how distributed the sales volumes per each play type in {week}",
    )
    fig_play_playtype.update_xaxes(showspikes=False)
    fig_play_playtype.update_yaxes(showspikes=False)
    fig_play_playtype.update_layout(
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
    )
    return fig_play_playtype


def get_fig_player_percentage(df, week="1"):
    fig_player_percentage = px.bar(
        df,
        x="play_type",
        y="pt_perc",
        color="player",
        text="player",
        title="What percentages of play types were sold for each player",
        labels=dict(
            play_type="Play Type", pt_perc="Percentage (%)", player="Player Name"
        ),
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig_player_percentage.update_layout(showlegend=False)
    return fig_player_percentage


def get_fig_platype_percentage(df, wek="1"):
    fig_playtype_percentage = px.bar(
        df,
        x="player",
        y="pl_perc",
        color="play_type",
        title="What player moments were popular in different play types.",
        labels=dict(
            play_type="Play Type", pl_perc="Percentage (%)", player="Player Name"
        ),
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig_playtype_percentage.update_xaxes(tickangle=35)
    fig_playtype_percentage.update_layout(
        hovermode="x unified",
        # legend=dict(yanchor="bottom", xanchor="left", y=-0.6, x=0, orientation="h"),
    )
    return fig_playtype_percentage
