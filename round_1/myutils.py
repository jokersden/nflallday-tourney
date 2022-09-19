import streamlit as st

# https://teamcolorcodes.com/nfl-team-color-codes/
team_colors = {
    "Arizona Cardinals": "#97233f",
    "Atlanta Falcons": "#a71930",
    "Baltimore Ravens": "#241773",
    "Buffalo Bills": "#00338d",
    "Carolina Panthers": "#0085ca",
    "Chicago Bears": "#0b162a",
    "Cincinnati Bengals": "#fb4f14",
    "Cleveland Browns": "#311d00",
    "Dallas Cowboys": "#041e42",
    "Denver Broncos": "#002244",
    "Detroit Lions": "#0076b6",
    "Green Bay Packers": "#203731",
    "Houston Texans": "#03202f",
    "Indianapolis Colts": "#002c5f",
    "Jacksonville Jaguars": "#006778",
    "Kansas City Chiefs": "#e31837",
    "Los Angeles Chargers": "#002a5e",
    "Los Angeles Rams": "#003594",
    "Miami Dolphins": "#008e97",
    "Minnesota Vikings": "#4f2683",
    "New England Patriots": "#002244",
    "New Orleans Saints": "#d3bc8d",
    "New York Giants": "#0b2265",
    "New York Jets": "#125740",
    "OAK": "#000000",
    "Philadelphia Eagles": "#004c54",
    "Pittsburgh Steelers": "#ffb612",
    "San Francisco 49ers": "#aa0000",
    "Seattle Seahawks": "#002244",
    "Tampa Bay Buccaneers": "#d50a0a",
    "Tennessee Titans": "#0c2340",
    "32	Washington Football Team": "#773141",
}


def human_format_single(num):
    magnitude = 0
    if float(num) >= 0:
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        num = f'{round(num, 2)} {["", "K", "M", "G", "T", "P"][magnitude]}'
    else:
        pass
    return num


def human_format(nums):
    for i, num in enumerate(nums):
        magnitude = 0
        if float(num) >= 0:
            while abs(num) >= 1000:
                magnitude += 1
                num /= 1000.0
            nums[i] = f'{round(num, 2)} {["", "K", "M", "G", "T", "P"][magnitude]}'
        else:
            nums[i] = num

    return nums


def get_chart_markdown(msg):
    return st.markdown(
        f"<div style='border: 1px solid #8d99ae; padding: 15px;'><span style='color:#8d99ae;'>{msg}</span></div>",
        unsafe_allow_html=True,
    )
