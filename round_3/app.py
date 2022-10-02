import streamlit as st
import pandas as pd

import nfl_data_py

import plotly.io as pio

from myutils import get_week_markdown, get_weekly_desc_markdown
from week1 import get_fig_q1
from metadata import week_1_data

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
    ttl=600 * 60,
    show_spinner=False,
    suppress_st_warning=True,
)
def load_data():
    with st.spinner(f"Steady lads, we're loading data...)"):
        df_week1 = None


st.markdown(
    """<div style='width: 100%; height: 150px; text-align: center; background-image: url("https://media.cnn.com/api/v1/images/stellar/prod/220905075016-01-nfl-glossary.jpg?c=16x9&q=h_270,w_480,c_fill");'><h1>🏈 NFL All Day - THE PLAYBOOK 🏈</h1></div></br></br>""",
    unsafe_allow_html=True,
)

# Week 1
intro, week1, week2, week3, week4, mt = st.tabs(
    ["Introduction", "Week 1", "Week 2", "Week 3", "Week 4", "Methodology"]
)
with intro:
    pass
with week1:
    get_week_markdown("Week 1")
    c1, c2 = st.columns([2, 6])
    get_weekly_desc_markdown(
        week_1_data["challenges"],
        c1,
    )
    c2.plotly_chart(get_fig_q1(None), use_container_width=True)
    st.selectbox("Select the challenge:", week_1_data["challenges"])

# Week 2
with week2:
    get_week_markdown("Week 2")

# Week 3
with week3:
    get_week_markdown("Week 3")

# Week 4
with week4:
    get_week_markdown("Week 4")
    c1, c2 = st.columns([8, 2])
