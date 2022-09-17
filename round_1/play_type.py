import plotly.express as px


def get_fig_moment_playtype(df, val_player):
    df_daily_sales_moment_playtype = (
        df.groupby(["play_type", "moment_tier"]).sum().reset_index()
    )
    fig_moment_playtype = px.bar(
        df_daily_sales_moment_playtype,
        x="play_type",
        y="total",
        color="moment_tier",
        text="total",
        title=f"What moments were most sought out {val_player}",
        labels=dict(play_type="Play Type", total="Amount (USD)", moment_tier="Tier"),
    )
    fig_moment_playtype.update_traces(
        hovertemplate="<br>".join(
            [
                "Play Type: %{x}",
                "Volume: $%{y:,.2f}",
            ]
        )
    )
    fig_moment_playtype.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig_moment_playtype
