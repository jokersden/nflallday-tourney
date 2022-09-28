import plotly.express as px
import plotly.graph_objects as go


def get_all_td_position(df):
    fig = px.bar(
        df.groupby(["PLAYERPOSITION", "td"]).sum().reset_index(),
        x="PLAYERPOSITION",
        y="TOTAL",
        color="td",
        custom_data=["td"],
        color_discrete_sequence=["sienna", "lightseagreen"],
        labels=dict(td="", PLAYERPOSITION="Player Position", TOTAL="Sales Volume($"),
    )
    fig.update_traces(
        hovertemplate="<br> <b>%{x}</b><br><br>"
        + "Touchdown status: %{customdata[0]} </br>"
        + "Volume Sold: $%{y:,.2f} <extra></extra>"
    )
    fig.update_xaxes(showspikes=False)
    fig.update_layout(
        hovermode="x unified",
        legend=dict(
            yanchor="top", xanchor="right", y=1.1, x=1, orientation="h", title=""
        ),
        # legend_title="",
    )
    return fig


def get_sankey_all(df):
    fig = px.parallel_categories(
        df[["PLAYERPOSITION", "PLAY_TYPE", "td", "winning"]],
        template="plotly_dark",
        # color=df["TOTAL"],
        labels=dict(
            PLAYERPOSITION="Player Position",
            td="Touchdown status",
            PLAY_TYPE="Play Type",
            winning="End result",
        ),
        title="How Player position and play type helped scoring touchdowns and finally contributing to the end result",
    )  # , color="PLAYER",
    return fig
