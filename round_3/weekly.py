import plotly.express as px


def get_fig_full_week(df, metadata):
    fig = px.bar(
        df,
        x="hour",
        y="price",
        labels=dict(hour="Date and Time", price="Sales Volume ($)"),
        title="All Moments sales during this week",
        color_discrete_sequence=[metadata["color"]],
    )
    for i, l in enumerate(metadata["times"]):
        fig.add_vrect(
            x0=l["start"],
            x1=l["end"],
            annotation_text=metadata["challenges"][i].split("-")[0],
            annotation_position="inside top right",
            annotation_textangle=-60,
            annotation_font_size=12,
            annotation_font_color="orange",
            annotation_font_family="Courier New, monospace, bold",
            fillcolor="yellow",
            line_color="white",
            opacity=0.08,
            line_width=1,
            line_dash="solid",
        )

        fig.add_vline(
            x=l["start"],
            line_color="yellow",
            line_width=2,
            line_dash="dash",
        )
        fig.add_vline(
            x=l["end"],
            line_color="yellow",
            line_width=2,
            line_dash="dash",
        )

    fig.update_layout(
        hovermode="x unified",
    )
    fig.update_xaxes(showspikes=False)
    return fig
