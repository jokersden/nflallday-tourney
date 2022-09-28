import pandas as pd
import streamlit as st

import nfl_data_py as nfl

import plotly.io as pio

from myutils import human_format_single, get_chart_markdown, col_metadata
from rush import (
    get_toprushes,
    get_rush_formation,
    get_rush_td_tot,
    get_rush_tot_player,
    get_win_total_box,
    get_win_avg_box,
    get_rush_avg_player,
    get_rush_by_position,
)
from all_td import get_all_td_position, get_sankey_all

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
st.markdown(hide_st_style, unsafe_allow_html=True)


@st.cache(
    allow_output_mutation=True,
    ttl=30 * 60,
    show_spinner=False,
    suppress_st_warning=True,
)
def load_data():
    with st.spinner(f"Steady lads, we're loading data...)"):
        return (
            pd.read_parquet(
                "https://github.com/jokersden/resources/blob/main/all_rush.parquet?raw=true"
            ),
            pd.read_parquet(
                "https://github.com/jokersden/resources/blob/main/all_tds.parquet?raw=true"
            ),
        )


st.markdown(
    """<div style='width: 100%; height: 150px; text-align: center; background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT18wkAdMZIhRiC1ZApgVCaX95-6niJxAe2JA&usqp=CAU");'><h1>🏈 NFL All Day 🏈</h1></div></br></br>""",
    unsafe_allow_html=True,
)

df, df_all = load_data()
st.success("This analysis consider only the NFT sales happened in 2022 season!.")
# tab1, tab2, tab3 = st.tabs(["🏃‍♂️ Rush", "b", "c"])

# with tab1:
st.subheader("Top 5 Rushing moments based on sales volume")
top5 = get_toprushes(df)
for i, vid in enumerate(list(st.columns(5))):
    vid.video(top5[0][i])
    vid.write(top5[1][i] + "- $" + str(human_format_single(top5[2][i])))
st.markdown("---")
st.subheader(
    "Does the rush ended up in a TD or a victory in the game, helps moment sales?"
)
r1, r2 = st.columns(2)
r1.plotly_chart(get_win_total_box(df), use_container_width=True)
r2.plotly_chart(get_win_avg_box(df), use_container_width=True)
get_chart_markdown(
    "🏃‍♂️<ul> <li> It's quite obvious that a moment from a winning game would generate higher volume of sales regardless of that rush ended up being a touchdown or not.</li>"
    + "<li> However, it's suprising to see that 2 of the most expensive moments(videos) were <b>in losing cause</b> and the most expensive one was a <b>non touch down and was in a losing cause too</b></li>"
    + "<li>however, their volumes were low, the most expensive moment was by Javonte Williams, $1624.50, however only two moments were sold, similarly Amon-Ra st. Brown's moment sold for $1620 but there was only 1 sale.</li>"
    + "<li>Which shows that although they were the expensive, they were not that popular or fan favorites, Also the non touchdowns in losing causes has a higher variance in price but low amounts in volumes.</li> <li><b>Could that suggest"
    + " there are certain players who played well but failed to help there teams victory had some great moments which certain die hard fans love?</b>.</li> <li><b>Anyway fans prefer to buy more and more moments which happened during victories.</b></li></ul>"
)

st.markdown("---")
st.write("")
st.subheader(
    "How player performance on a particular moment and it's outcome impact the sales of the moments"
)
col = st.selectbox(
    "Select a metric from the dropdown below: ",
    col_metadata.keys(),
)

st.plotly_chart(
    get_rush_tot_player(df, col_metadata[col]["name"], col),
    use_container_width=True,
)
st.plotly_chart(
    get_rush_avg_player(df, col_metadata[col]["name"], col),
    use_container_width=True,
)
get_chart_markdown(
    """🏃 Victories: <i>(Select the metrics from the drop down to visualize the results)</i><ul><li>Nick Chubb seems to have pretty even volumes of sales in both winning and losing games, but the average price of a moment in a winning game is almost <b>40X</b> than in a losing match.</li>
    <li>There are multiple players with all their best moments in losing matches however, only <b>Joe Mixon</b> has his losing side moments are expensive than the winning side among players having moments sold in both winning and losing, BUT volume wise only 3 of his losing side moments were sold.</li></ul>
    🏃 Scoring a Touchdown<ul><li>Again Nick Chubb has so many of his moments sold which weren't ended up being a TD. However, the average price of non TD moments were very low but number of sales are pretty high. Do people love Chubb? Or has he done amazingly while his team performs poorly?</li>
    <li>It's clear that higher the average price, lower the sales volume regardless of the outcome of the game or that particular play.</li></ul>
    🏃 Rushing Yards<ul><li>Number of yards that th rush doesn't seem to correlate with the volume of sale but it looks like the average price of the moment is higher when the rushing yards are higher (We will confirm this thesis in the next chart)</li></ul>"""
)
st.plotly_chart(get_rush_td_tot(df), use_container_width=True)
get_chart_markdown(
    """🏃‍♂️ (Size of the circle denotes the average price paid for that moment.)
    <ul><li>Well the moments with more rushing yards ended up being in touchdowns and on average their average prices are relatively higher than the rest, although the sales volumes are lower. (except for the highest rushing yard TD moment, which was interestingly has a low average price as well as a low sales volume).</li>
    </ul>
    """
)
st.markdown("---")
st.plotly_chart(get_rush_formation(df), use_container_width=True)
st.markdown(
    "<h5>What effect does it have on sales and average price based on player position and touchdown status of a RUSH?</h5>",
    unsafe_allow_html=True,
)
ch1, ch2 = st.columns(2)
ch1.plotly_chart(get_rush_by_position(df, "TOTAL"), use_container_width=True)
ch2.plotly_chart(get_rush_by_position(df, "AVG_PRICE"), use_container_width=True)
get_chart_markdown(
    """🏃 <ul>
    <li>RB players have accounted for more moments in rushes than anybody else. In terms of both number of moments (2/3 of number of moments) and sales volume.</li>
    <li>Moments with touchdown of RB players seems to have enjoyed more favorism from fans as it has larger sales volume than others, even the average price of a moment is higher except for WR's moments with touchdowns.</li>
    <li>QBs have a higher percentage of their moments sales in non touchdown events, also their non touchdown moments have an higher average price than their touchdown moments.</li>
    </ul>
    """
)
st.markdown("---")
st.subheader("What about ALL the TOUCHDOWNs not just rush TDs")
st.plotly_chart(get_all_td_position(df_all), use_container_width=True)
get_chart_markdown(
    """🏃 <ul>
    <li>Apart from QB, RB, WR, and TE(?) the other positions have significantly low touchdown moments in terms of sales volume in this season so far.</li>
    <li>Again the usual suspects, QB, RB, and WR leading the sales charts with higher volume of sales, and there moments sales seems to have evenly distributed among TD and non TD events.</li>
    <li>When comparig OL with DL we see that both have comparably lower sales volumes, however DL has 48X times higher sales volume and <b>nearly 97% of these amounts were spent on moments that were ended up in no touchdowns</b></li>
    <li>OL have very limited sales volume and from the little they had 2/3 were in non TD moments.</li>
    </ul?"""
)
st.plotly_chart(get_sankey_all(df_all), use_container_width=True)
get_chart_markdown(
    """🏃 <ul>
    <li>While RB dominated the sales volume in rush moments we can see that WR are the overall winner in terms of number of distinct moments(videos) sold during this season.</li>
    <li>Reception moments seems to be something fans love, as 38% of these 574 moments were Reception moments</li>
    <li>WR's receptions which ended up with a TD and contributed to teams victory were among fans most favorite moments, in terms of number of such moments, but comparedto sales volume, losing cause TDs</li>
    <li>All 40 of the Sack play moments were NON TDs</li>
    </ul>"""
)
st.write("")
get_chart_markdown(
    """🏈 Conclusion: </br>
    Fans rule the game, even though the players are the once who made all the fun. During 2022 season of NFL, the fans had shown their interest in their favorite players. While touchdowns were pretty important for QB, RB, and WRs moments to be liked by
    their fans, in general there were more Non TD moments than TD moments being sold during this season. However, resulting in a touchdown shows an increase in volume and specially average price of that moment than non touchdowns. 
    Specially in rushing moments we saw that some players do had their moments sold regardless of being a non touchdown and also in a losing, probably they were either fan favorites but unfortunately in a poor performing team?. All in all it's quite clear that
    performances which help their own teams victory make precious moments that fans would love to through their money at.
    """
)

st.markdown("---")
with st.expander("Methodology", True):
    st.markdown(
        """In this analysis first we looked at how the rushing moments were sold in this 2022 season and then analysed the touchdowns by all play types. 
        Since it's the play that we were interested in I had analysed distinct videos (moments) which is the real moment of that play (<b>thus group by video_id not nflallday_id</b>). 
        Please note that one video can have multiple NFTs in a collection, I considered average price, sales volume for all the NFTs per video. 
        Since touchdown status was not available in Flipside, I used nfl_data_py package to query whether the play ended up being a touchdown and the number of yards the player rushed. 
        There were 79 distinct moments(videos) of rushing moments and then 574 distinct moments were being analysed.
        Following is the query used to get data: 
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """```sql
        with sales as (
select 
    nft_collection,
    nft_id,
    sum(price) as total,
    count(tx_id) as sales,
    count(buyer) as buyers,
    count(seller) as sellers,
    avg(price) as avg_price
from flow.core.ez_nft_sales
    where 
        block_timestamp::date >= '2022-9-8'
    group by 
        nft_collection, 
        nft_id
)
select 
    count(distinct nflallday_id) as distinct_nfts,
    count(m.nft_id) as nfts,
    min(moment_tier) as moment_tier,
    min(player) as player,
    min(team) as team,
    min(season) as season,
    min(week) as week,
    min(classification) as classification,
    min(play_type) as play_type,
    min(moment_date) as moment_date,
    min(series) as series,
    min(set_name) as set_name,
    moment_stats_full:id as video_id, 
    min(moment_stats_full:metadata:awayTeamName) as awayteam,
    min(moment_stats_full:metadata:awayTeamScore) as awayteamscore, 
    min(moment_stats_full:metadata:gameDate) as gamedate,
    min(moment_stats_full:metadata:gameTime) as gametime,
    min(moment_stats_full:metadata:gameDistance) as gamedistance,
    min(moment_stats_full:metadata:gameDown) as gamedown,
    min(moment_stats_full:metadata:gameQuarter) as gamequarter,
    min(moment_stats_full:metadata:playerPosition) as playerposition,
    min(moment_stats_full:metadata:homeTeamName) as hometeamname,
    min(moment_stats_full:metadata:homeTeamScore) as hometeamscore,
    min(moment_stats_full:metadata:images) as images,
    min(moment_stats_full:metadata:description) as description,
    min(moment_stats_full:metadata:playerID) as player_id,
    sum(total) as total,
    sum(sales) as sales,
    sum(buyers) as buyers,
    sum(sellers) as sellers,
    avg(avg_price) as avg_price
from flow.core.dim_allday_metadata m
    inner join 
        sales s on m.nft_collection=s.nft_collection and m.nft_id=s.nft_id
    group by video_id
    """
    )
