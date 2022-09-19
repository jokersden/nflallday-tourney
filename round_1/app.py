import math
import os

import pandas as pd
import streamlit as st

from shroomdk import ShroomDK
import nfl_data_py as nfl

import plotly.io as pio

from play_type import get_fig_moment_playtype
from play_player import get_fig_play_playtype, get_fig_player_percentage
from player import get_fig_player_total, get_fig_playaer_stats, get_top5_players
from myutils import get_chart_markdown, team_colors
from play_player import get_fig_platype_percentage
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
st.markdown(hide_st_style, unsafe_allow_html=True)


st.success("Please Note: All the dates and time are in US/New York time.", icon="⏰")


@st.cache(
    allow_output_mutation=True,
    ttl=30 * 60,
    show_spinner=False,
    suppress_st_warning=True,
)
def load_data(data):

    with st.spinner(
        f"Hey Hey!! {data['msg']} (ShroomDK may take a few minutes to load data...)"
    ):
        page_count = pd.DataFrame(
            sdk.query(
                f"""
    select 
        count(*) as pages
    from flow.core.ez_nft_sales s
        inner join flow.core.dim_allday_metadata m 
            on m.nft_collection=s.nft_collection 
            and m.nft_id=s.nft_id
    where 
        date_trunc(hour, convert_timezone('UTC', 'America/New_York', block_timestamp::timestamp_ntz))::date >= '{data["start_date"].strftime("%Y-%m-%d")}'
        and date_trunc(hour, convert_timezone('UTC', 'America/New_York', block_timestamp::timestamp_ntz))::date <= '{data["end_date"].strftime("%Y-%m-%d")}' 
        and TX_SUCCEEDED='TRUE'
    """,
            ).records
        ).pages.values[0]

        sql = f"""
    select 
        date_trunc(hour, convert_timezone('UTC', 'America/New_York', block_timestamp::timestamp_ntz)) as hour,
        nflallday_id, 
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
        MOMENT_STATS_FULL:metadata:playerID as player_id,
        MOMENT_STATS_FULL:id as video_id,
        replace(lower(set_name), ' ', '_') as set_name,
        price, 
        seller,
        buyer, 
        tx_id as sales 
    from flow.core.ez_nft_sales s
        inner join flow.core.dim_allday_metadata m 
            on m.nft_collection=s.nft_collection 
            and m.nft_id=s.nft_id
    where 
        hour::date >= '{data["start_date"].strftime("%Y-%m-%d")}'
        and hour::date <= '{data["end_date"].strftime("%Y-%m-%d")}' 
        and TX_SUCCEEDED='TRUE' 
    order by block_timestamp
    """

        if page_count <= 100_000:
            df_all = pd.DataFrame(
                sdk.query(
                    sql,
                ).records
            )
        else:
            for i in range(math.ceil(page_count / 100_000)):
                query_results = sdk.query(
                    sql,
                    page_number=i + 1,
                ).records

                if i == 0:
                    df_all = pd.DataFrame(query_results)
                else:
                    df_all = pd.concat([df_all, pd.DataFrame(query_results)])

    return pd.merge(
        df_all,
        nfl.clean_nfl_data(
            pd.merge(
                nfl.import_seasonal_data([2022]),
                nfl.import_rosters([2022]),
                on="player_id",
            )
        ),
        on="player_id",
    )


col1, col2, col3 = st.columns(3)
with col1:
    week = st.selectbox("Please select a week", tuple(meta_data.keys()), 1)

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
        l.video(df_vids[0].video_url.values[i])
        l.markdown(
            f"<div width=100% style='display: flex; justify-content:center; flex-direction:row;'><span style='text-align: center; color: red;'>{df_vids[0].player.values[i]} - {df_vids[0].play_type.values[i]} in {df_vids[0].season.values[i]}</span></div>",
            unsafe_allow_html=True,
        )
    st.markdown("---")
    ch1, ch2 = st.columns(2)
    with ch1:
        st.plotly_chart(
            get_fig_moment_playtype(df_allday, week), use_container_width=True
        )
        get_chart_markdown(
            "Above chart shows what play type moments were sold, how many sales happened for each play type, and how much in dollar terms they cost. The color represents the average price per moment in each play type."
            + "</br>         </br>"
        )
    with ch2:
        st.plotly_chart(
            get_fig_player_total(df_allday, week),
            use_container_width=True,
        )
        get_chart_markdown(
            "This shows what players were the top 20 in terms of the volume of sales, and how many sales happened for each player in this top 20, and how much in dollar terms they cost. The color represents the average price per moment per player."
        )

    st.markdown("---")

    pch1, pch2 = st.columns(2)
    df_pt_pl = (
        df_allday.groupby(["play_type", "player"])
        .agg(
            total=("price", "sum"),
            avg_price=("price", "mean"),
            sales=("sales", "count"),
        )
        .reset_index()
        .sort_values(by="total", ascending=False)
    )
    df_pt_sum = df_pt_pl.groupby("play_type").sum().reset_index()
    df_pl_sum = df_pt_pl.groupby("player").sum().reset_index()

    df_pt_pl["pt_perc"] = df_pt_pl.apply(
        lambda x: (
            x.total * 100 / df_pt_sum[df_pt_sum.play_type == x.play_type]["total"].sum()
        ),
        axis=1,
    )
    df_pt_pl["pl_perc"] = df_pt_pl.apply(
        lambda x: (
            x.total * 100 / df_pl_sum[df_pl_sum.player == x.player]["total"].sum()
        ),
        axis=1,
    )
    with pch1:
        st.plotly_chart(get_fig_platype_percentage(df_pt_pl), use_container_width=True)
        get_chart_markdown(
            "This shows in terms of sales volume what percentage each player sold in different play types. Are the certain players mostly favorited in certain play types?"
            + "</br>         </br>"
        )
    with pch2:
        st.plotly_chart(
            get_fig_play_playtype(df_allday, week), use_container_width=True
        )
        get_chart_markdown(
            "Different play types have different amounts of sold items and different players may have involved with different play types, This shows how distributed the moment prices are, also among different tiers in each play type."
        )

    st.plotly_chart(get_fig_player_percentage(df_pt_pl), use_container_width=True)
    get_chart_markdown(
        "How to read the above chart:  This shows which player and what percentage they of that particular play type were theirs"
        + ", in other words who are the players that stand outs in different play types based on their sales volume of All Day moments."
    )

    st.write("")
    st.markdown("---")
    stat_names = {
        "Rushing Yards": "rushing_yards",
        "Passing Yards": "passing_yards",
        "Completions": "completions",
        "Attempts": "attempts",
        "Receiving Yards": "receiving_yards",
    }
    st.subheader("Top 5 fan favorite players based on their moment sales")
    fantasy_players, radars = get_top5_players(df_allday)
    for i, im in enumerate(st.columns(5)):
        im.image(list(fantasy_players.headshot_url.values)[i])
        im.markdown(
            f""" <div width=100% style='display: flex; justify-content:center; flex-direction:row;'>
            <div>{list(fantasy_players.player.values)[i] + " - " }</div> 
            <div style='color: {team_colors[list(fantasy_players.team.values)[i]]};'>{list(fantasy_players.team.values)[i]} </div> 
            </div>
            <div> </div>""",
            unsafe_allow_html=True,
        )
        pl_vals = df_pt_pl[
            df_pt_pl.player == fantasy_players.player.values[i]
        ].nlargest(1, "pl_perc")[["play_type", "pl_perc", "total"]]
        im.markdown(
            f""" <div width=100% style='color: #0096c7; text-align: center; display: flex; justify-content:center; flex-direction:column;'>
        <div width=100% style='text-align: center;'>His Most popular AllDay Play type:</div> 
        <div width=100% style='text-align: center;'>{pl_vals.play_type.values[0]} - {round(pl_vals.pl_perc.values[0], 2)}%</div>
        <div width=100% style='text-align: center;'>Total sold: ${pl_vals.total.values[0]}</div> 
        </div>
        """,
            unsafe_allow_html=True,
        )
        im.plotly_chart(radars[i], use_container_width=True)
    get_chart_markdown(
        "Above radar charts per player shows their performances so far in this season, What percentile are their performances in, e.g: if somebosy has 0.9 for Passing Yards and 0.6 for Rushing Yards, that means that player is in the top 90% of the players so far in Passing Yards and in top 60% in Rushing Yards."
    )
    st.markdown("---")
    st.write("")
    stat = st.selectbox(
        "Pick one that you want to see the top players for: ",
        [
            "Rushing Yards",
            "Passing Yards",
            "Completions",
            "Attempts",
            "Receiving Yards",
        ],
    )

    st.plotly_chart(
        get_fig_playaer_stats(df_allday, stat_names[stat], stat, week),
        use_container_width=True,
    )
    st.markdown("---")
