import os
from datetime import datetime
import pandas as pd
import numpy as np
import streamlit as st

from shroomdk import ShroomDK

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
from videos import get_top_videos

from week_data import meta_data

pio.templates.default = "plotly_dark"

API_KEY = os.getenv("API_KEY")
sdk = ShroomDK(API_KEY)

st.set_page_config(
    page_title="NFL All Day",
    page_icon=":football:",
    layout="wide",
    menu_items=dict(About="it's a work of joker#2418"),
)

st.image(
    "https://thelowestask.files.wordpress.com/2021/12/all-day.png?w=1500&h=500&crop=1",
    use_column_width=True,
)

st.title(":football: NFL All Day :football:")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
# st.markdown(hide_st_style, unsafe_allow_html=True)


st.success("Please Note: All the dates and time are in US/New York time.", icon="⏰")


@st.cache(allow_output_mutation=True, ttl=30 * 60, show_spinner=False)
def load_data(data):
    with st.spinner(f"Hey you!! {data['msg']}"):
        return pd.DataFrame(
            sdk.query(
                f"""
    select 
        date_trunc(hour, convert_timezone('UTC', 'America/New_York', block_timestamp::timestamp_ntz)) as hour, 
        moment_tier, 
        player, 
        team, 
        season, 
        week,
        play_type,
        MOMENT_STATS_FULL:metadata:playerPosition as player_position,
        MOMENT_STATS_FULL:metadata:gameDate as moment_game_date,
        MOMENT_STATS_FULL:metadata:images as images,
        MOMENT_STATS_FULL:metadata:playerBirthdate as birthdate,
        MOMENT_STATS_FULL:metadata:playerBirthplace as birthplace,
        MOMENT_STATS_FULL:metadata:playerCollege as player_college,
        MOMENT_STATS_FULL:metadata:playerRookieYear as rookie_year,
        MOMENT_STATS_FULL:id as video_id,
        replace(lower(set_name), ' ', '_') as set_name,
        avg(price) as avg_price, 
        sum(price) as total, 
        count(distinct seller) as sellers,
        count(distinct buyer) as buyers, 
        count(distinct tx_id) as sales 
    from flow.core.ez_nft_sales s
        inner join flow.core.dim_allday_metadata m 
            on m.nft_collection=s.nft_collection 
            and m.nft_id=s.nft_id
    where 
        hour::date >= '{data["start_date"].strftime("%Y-%m-%d")}'
        and hour::date <= '{data["end_date"].strftime("%Y-%m-%d")}' 
        and TX_SUCCEEDED='TRUE'
    group by hour, moment_tier, player, team, season, video_id, set_name,
    week, play_type, player_position, moment_game_date, images, birthdate, 
    birthplace, player_college, rookie_year 
    order by hour
    """
            ).records
        )


col1, col2, col3 = st.columns(3)
with col1:
    week = st.selectbox("Please select a week", tuple(meta_data.keys()))

col2.metric(
    f"{week} strated :", str(meta_data[week]["start_date"].strftime("%Y-%B-%d"))
)
col3.metric(f"{week} ended :", str(meta_data[week]["end_date"].strftime("%Y-%B-%d")))
if week == "Preseason":
    st.info(
        "Please note that Preseason includes data till 7th Sept, Although it ended on 28th of August"
    )
df_allday = load_data(meta_data[week])
if len(df_allday) == 0:
    st.error("No data yet for this week...")
else:
    df_allday.hour = pd.to_datetime(df_allday.hour)
    df_vids = get_top_videos(df_allday)

    st.subheader(f"This week's top selling fan favorite moments [{week}]")
    for i, l in enumerate(list(st.columns(5))):
        l.video(df_vids[i])
