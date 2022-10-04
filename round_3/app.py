import streamlit as st
import pandas as pd

import nfl_data_py

import plotly.io as pio

from myutils import get_week_markdown, get_weekly_desc_markdown, get_chart_markdown
from weekly import get_fig_full_week
from week1 import get_fig_q1, get_fig_q1_crash, get_fig_q1_crash_box, get_fig_q2
from metadata import week_1_data, week_2_data, week_3_data, week_4_data, week_5_data

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
def load_data(url, date_col="hour"):
    with st.spinner(f"Steady lads, deploying some data...)"):
        df = pd.read_csv(
            "https://drive.google.com/uc?export=download&id=" + url.split("/")[-2]
        )
        if date_col:
            df[date_col] = pd.to_datetime(df[date_col])
        return df


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
    df_full_week1 = load_data(
        "https://drive.google.com/file/d/1lUPneGPi0lPSw62FI0aViuZYYj-edYPF/view?usp=sharing"
    )
    get_week_markdown("Week 1")
    c1, c2 = st.columns([2, 6])
    get_weekly_desc_markdown(
        week_1_data["challenges"],
        c1,
    )
    c2.plotly_chart(
        get_fig_full_week(
            df_full_week1,
            week_1_data,
        ),
        use_container_width=True,
    )
    get_chart_markdown(
        """🏈 This shows all the sales happened through out the week, including all the 5 challenges in this week..
    <li>In terms of the sales volumes ($ value of the moments) seems to have picked up in patches, some of these high volumes overlap quite well with the challenge timeframes, while the game playing hours seems to be so common time period.</li>
    <li>Are the people who buying just to participate in the challenge buying the low price moments vs the rest of moment collectors?</li>
    """
    )
    st.markdown("---")
    chl = st.selectbox(
        "Select the challenge for the dropdown below:", week_1_data["challenges"]
    )
    if chl == week_1_data["challenges"][0]:
        df_week1_ch1 = load_data(
            "https://drive.google.com/file/d/1-Et_0rhodkDGzZtOkj0yStCOl-drf5_L/view?usp=sharing"
        )
        st.markdown(week_1_data["challenge_text"][0])
        st.plotly_chart(get_fig_q1(df_week1_ch1, week_1_data), use_container_width=True)
        get_chart_markdown(
            """🏈 This includes the number of moment sales which were necessary only for Challenge 1.
        <li>It seems that there was a interest in people to buy all 4 necessary moments and highly likely participate in the challenge.</li>
        <li>Highest number of people (110 people) bought all the 4 necessary moments at the start of the challenge but the rate picked up since the start of the game between Biils vs Rams.</li>
        <li>Then the buying of all these 4 moments by a fan has decreased since, understandably after the challenge ended.</li>
        <li>So, it's quite evident that people have started buying the moments to participate in the challenge during the game but trend picked up towards the challenge start and slowed a bit until the end of the challenge.</li>
        """
        )

        st.markdown("---")
        df_ch1_nfts = load_data(
            "https://drive.google.com/file/d/1Ef5LnRFiu5fpJ2fRgyLHgBjcC_ELBiPu/view?usp=sharing",
            None,
        )
        crashcol1, crashcol2 = st.columns([2, 1])
        crashcol1.plotly_chart(get_fig_q1_crash(df_ch1_nfts), use_container_width=True)
        crashcol2.plotly_chart(
            get_fig_q1_crash_box(df_ch1_nfts), use_container_width=True
        )
        get_chart_markdown(
            """🏈 Out of the NFTs sold in this week what percentage of NFTs did crash price?
            <li></li>
            """
        )

    elif chl == week_1_data["challenges"][1]:
        st.info(
            "unlike in week 1, there were NO one buying all (8) of their necessary moments from the secondary market in week 2. So we'll be looking at all the sales which matches either of the conditions."
        )
        df_week1_ch2 = load_data(
            "https://drive.google.com/file/d/1-2MuLehtbhFuDA-iHfD-uPF4GGdsYiXm/view?usp=sharing"
        )
        st.markdown(week_1_data["challenge_text"][1])
        st.plotly_chart(get_fig_q2(df_week1_ch2, week_1_data), use_container_width=True)
    elif chl == week_1_data["challenges"][2]:
        st.markdown(week_1_data["challenge_text"][2])
    elif chl == week_1_data["challenges"][3]:
        st.markdown(week_1_data["challenge_text"][3])
    elif chl == week_1_data["challenges"][4]:
        st.markdown(week_1_data["challenge_text"][4])

# Week 2
with week2:
    df_full_week2 = load_data(
        "https://drive.google.com/file/d/1dlT64EQ7u8E1CVyOeluExMvt_eVxYVuw/view?usp=sharing"
    )
    get_week_markdown("Week 2")

    w2c1, w2c2 = st.columns([2, 6])
    get_weekly_desc_markdown(
        week_2_data["challenges"],
        w2c1,
    )
    w2c2.plotly_chart(
        get_fig_full_week(
            df_full_week2,
            week_2_data,
        ),
        use_container_width=True,
    )
    get_chart_markdown(
        """🏈 This shows all the sales happened through out the week, including all the 5 challenges in this week..
    <li>In terms of the sales volumes ($ value of the moments) seems to have picked up in patches, some of these high volumes overlap quite well with the challenge timeframes, while the game playing hours seems to be so common time period.</li>
    <li>Are the people who buying just to participate in the challenge buying the low price moments vs the rest of moment collectors?</li>
    """
    )
    st.markdown("---")

# Week 3
with week3:
    df_full_week3 = load_data(
        "https://drive.google.com/file/d/1lUPneGPi0lPSw62FI0aViuZYYj-edYPF/view?usp=sharing"
    )
    get_week_markdown("Week 3")

    w3c1, w3c2 = st.columns([2, 6])
    get_weekly_desc_markdown(
        week_3_data["challenges"],
        w3c1,
    )
    w3c2.plotly_chart(
        get_fig_full_week(
            df_full_week3,
            week_3_data,
        ),
        use_container_width=True,
    )
    get_chart_markdown(
        """🏈 This shows all the sales happened through out the week, including all the 5 challenges in this week..
    <li>In terms of the sales volumes ($ value of the moments) seems to have picked up in patches, some of these high volumes overlap quite well with the challenge timeframes, while the game playing hours seems to be so common time period.</li>
    <li>Are the people who buying just to participate in the challenge buying the low price moments vs the rest of moment collectors?</li>
    """
    )
    st.markdown("---")

# Week 4
with week4:
    df_full_week4 = load_data(
        "https://drive.google.com/file/d/1lUPneGPi0lPSw62FI0aViuZYYj-edYPF/view?usp=sharing"
    )
    get_week_markdown("Week 4")

    w4c1, w4c2 = st.columns([2, 6])
    get_weekly_desc_markdown(
        week_4_data["challenges"],
        w4c1,
    )
    w4c2.plotly_chart(
        get_fig_full_week(
            df_full_week4,
            week_4_data,
        ),
        use_container_width=True,
    )
    get_chart_markdown(
        """🏈 This shows all the sales happened through out the week, including all the 5 challenges in this week..
    <li>In terms of the sales volumes ($ value of the moments) seems to have picked up in patches, some of these high volumes overlap quite well with the challenge timeframes, while the game playing hours seems to be so common time period.</li>
    <li>Are the people who buying just to participate in the challenge buying the low price moments vs the rest of moment collectors?</li>
    """
    )
    st.markdown("---")
