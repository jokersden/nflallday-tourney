from metadata import week_1_data

import plotly.express as px
import plotly.graph_objects as go


def get_fig_bar_data(df, metadata, i, title):
    fig = px.bar(
        df,
        x="hour",
        y="team",
        color="player",
        custom_data=["player", "price"],
        color_discrete_sequence=px.colors.sequential.haline_r,
        labels=dict(
            hour="Date Time",
            team="Number of moment sales",
            price="Sales Volume ($)",
            player="Player Name",
        ),
        title=title,
    )

    fig.add_vline(
        x=metadata["times"][i]["start"],
        line_color="yellow",
        line_width=2,
        line_dash="dash",
    )
    fig.add_annotation(
        x=metadata["times"][i]["start"],
        y=100,
        text=f"Challenge start",
        yanchor="top",
        xanchor="left",
        showarrow=True,
        arrowhead=1,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#636363",
        font=dict(size=14, color="blue", family="Courier New, monospace, bold"),
        bordercolor="green",
        borderwidth=2,
        bgcolor="#CFECEC",
        opacity=0.6,
    )
    fig.add_vline(
        x=metadata["times"][i]["end"],
        line_color="yellow",
        line_width=2,
        line_dash="dash",
    )
    fig.add_annotation(
        x=metadata["times"][i]["end"],
        y=100,
        text=f"Challenge end",
        yanchor="top",
        xanchor="left",
        showarrow=True,
        arrowhead=1,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#636363",
        font=dict(size=14, color="blue", family="Courier New, monospace, bold"),
        bordercolor="green",
        borderwidth=2,
        bgcolor="#CFECEC",
        opacity=0.6,
    )

    fig.update_traces(
        hovertemplate="<b>%{customdata[0]}</b><br>"
        + "Number of sales: %{y} - $%{customdata[1]}<extra></extra>"
    )
    fig.update_layout(
        hovermode="x unified",
    )
    fig.update_xaxes(showspikes=False)

    return fig


def get_fig_q1(df, metadata):
    df = (
        df[(df.team == "Buffalo Bills") | (df.team == "Los Angeles Rams")]
        .groupby(["hour", "player"])
        .agg({"team": "count", "price": "sum"})
        .reset_index()
    )
    return get_fig_bar_data(
        df, metadata, 0, title="How many fans bought all necessary moments."
    )


def get_fig_q2(df, metadata):
    df = (
        df.groupby(["hour", "player"])
        .agg({"team": "count", "price": "sum"})
        .reset_index()
    )
    return get_fig_bar_data(df, metadata, 1, title="How many fans bought supplies.")


def get_fig_q1_crash(df):
    df = df.groupby(["player", "crashed"]).count().reset_index()
    df["crash_perc"] = (
        100 * df["total"] / df.groupby("player")["total"].transform("sum")
    )
    df = df.fillna("Yes")
    fig = px.area(
        df,
        x="player",
        y="crash_perc",
        color="crashed",
        color_discrete_sequence=["limegreen", "orangered"],
        custom_data=["crashed", "nft_id"],
        labels=dict(
            crash_perc="Percentage of NFTs(%)",
            player="Player Name",
            crashed="Price Crashed?",
        ),
        title="What percentage of NFTs crashed in prices for each player",
    )
    fig.update_traces(
        hovertemplate="<b>%{y:.2f}%</b><br>"
        + "Price dropped? %{customdata[0]}<br>"
        + "Number of NFTs: %{customdata[1]}<extra></extra>"
    )
    fig.update_layout(
        hovermode="x unified",
        legend=dict(
            yanchor="top",
            xanchor="right",
            y=1.1,
            x=1,
            orientation="h",
            title="Crashed?",
        ),
    )
    fig.update_xaxes(showspikes=False)

    return fig


def get_fig_q1_crash_box(df):
    fig = px.box(
        df,
        y="chng",
        color="crashed",
        title="How strong the price drops vs price gains",
        labels=dict(chng="Change Percentage(%)"),
    )
    fig.update_traces(
        hovertemplate="<b>%{y:.2f}%</b><br>"
        + "Price dropped? %{customdata[0]}<br>"
        + "Number of NFTs: %{customdata[1]}<extra></extra>"
    )
    fig.update_layout(
        hovermode="x unified",
        legend=dict(
            yanchor="top",
            xanchor="right",
            y=1.1,
            x=1,
            orientation="h",
            title="Crashed?",
        ),
    )
    fig.update_xaxes(showspikes=False)
    return fig


def get_fig_q2(df, metadata):
    df = (
        df[(df.team == "Buffalo Bills") | (df.team == "Los Angeles Rams")]
        .groupby(["hour", "player"])
        .count()
        .reset_index()
    )
    return get_fig_bar_data(df, metadata, 1)
