import streamlit as st

col_metadata = {
    # "Sales Volume": {"name": "TOTAL"},
    # "NFT Price": {"name": "AVG_PRICE"},
    "Winning": {"name": "winning"},
    "Touchdown": {"name": "rush_touchdown_enc"},
    "Rushing Yards": {"name": "rushing_yards"},
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


def get_chart_markdown(msg):
    return st.markdown(
        f"<div style='border: 1px solid #8d99ae; padding: 15px;'><span style='color:#8d99ae;'>{msg}</span></div>",
        unsafe_allow_html=True,
    )
