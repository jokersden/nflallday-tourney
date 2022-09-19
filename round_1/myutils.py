import streamlit as st


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
