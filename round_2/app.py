import pandas as pd
import streamlit as st

import nfl_data_py as nfl

import plotly.io as pio

from myutils import human_format_single, get_chart_markdown
from rush import get_toprushes, get_rush_formation, get_rush_td_tot, get_rush_td_player

pio.templates.default = "plotly_dark"

st.set_page_config(
    page_title="NFL All Day",
    page_icon=":football:",
    layout="wide",
    menu_items=dict(About="it's a work of joker#2418"),
)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
# st.markdown(hide_st_style, unsafe_allow_html=True)
@st.cache(
    allow_output_mutation=True,
    ttl=30 * 60,
    show_spinner=False,
    suppress_st_warning=True,
)
def load_data():
    with st.spinner(f"Steady lads, we're loading data...)"):
        return pd.read_parquet("data/all_rush.parquet")


st.markdown(
    """<div style='width: 100%; height: 150px; text-align: center; background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT18wkAdMZIhRiC1ZApgVCaX95-6niJxAe2JA&usqp=CAU");'><h1>🏈 NFL All Day 🏈</h1></div></br></br>""",
    unsafe_allow_html=True,
)

df = load_data()
tab1, tab2, tab3 = st.tabs(["🏃‍♂️ Rush", "b", "c"])

with tab1:
    st.subheader("Top 5 Rushing moments based on sales volume")
    top5 = get_toprushes(df)
    for i, vid in enumerate(list(st.columns(5))):
        vid.video(top5[0][i])
        vid.write(top5[1][i] + "- $" + str(human_format_single(top5[2][i])))
    st.markdown("---")
    r1, r2 = st.columns(2)
    r1.plotly_chart(get_rush_formation(df), use_container_width=True)
    r2.plotly_chart(get_rush_td_player(df), use_container_width=True)
    get_chart_markdown("🏃‍♂️ This is a test")
    st.plotly_chart(get_rush_td_tot(df), use_container_width=True)
    get_chart_markdown("🏃‍♂️ This is a test")

    st.markdown("---")
    with st.expander("Methodology"):
        st.write("test")
