import streamlit as st


def get_chart_markdown(msg):
    return st.markdown(
        f"<div style='border: 1px solid #8d99ae; padding: 15px;'><span style='color:#8d99ae;'>{msg}</span></div>",
        unsafe_allow_html=True,
    )


def get_week_markdown(msg):
    return st.markdown(
        f"<div style='border: 4px dotted #8da9ae; padding: 1px; width: 100%; display: flex; justify-content: center;'><H3 style='color:#8db9ae;'>{msg}</H3></div>",
        unsafe_allow_html=True,
    )


def get_weekly_desc_markdown(data, comp):
    html = ""
    for e in data:
        html += "<li>" + e + "</li>"
    return comp.markdown(
        f"<div style='height: 60vh; display: flex; border: 1px solid #8d99ae; padding: 15px; margin: 15px 0px 0px 0px;'><ul style='height: 100%; color:#82b9ae;'>{html}</ul></div>",
        unsafe_allow_html=True,
    )
