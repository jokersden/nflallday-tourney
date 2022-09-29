import streamlit as st
import pandas as pd
from docarray import Document

server_url = 'grpcs://dalle-flow.dev.jina.ai'

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

st.title(":football: NFL All Day Moments through Machine's eye :football:")
st.success("Let's look at what DALL.E perceive on NFL moment description.")
st.info("Please wait around 40s - 1 min for an image to be generated.. Thanks!. You can pick a moment from below drop down to generate new images..")
@st.cache(
    allow_output_mutation=True,
    ttl=30 * 60,
    show_spinner=False,
    suppress_st_warning=True,
)
def load_data():
    with st.spinner('Loading data'):
        df = pd.read_csv('https://github.com/jokersden/resources/blob/main/dataset_img.csv?raw=true')
    return df

df = load_data()
df['label'] = df.PLAYER + ' - ' + df.TEAM + ' in ' + df.SEASON.astype(str)

value = st.selectbox("Select a moment :", df.label.values)

prompt = df.loc[df.label == value, "DESCRIPTION"].head(1).values[0]

with st.spinner("Image is being generated!! please wait"):
    doc = Document(text=prompt).post(server_url, parameters={'num_images': 2})
    da = doc.matches

for i, im in enumerate(st.columns(4)):
    im.image(da[i].uri)
st.markdown("<h5>" + prompt + "</h5>", unsafe_allow_html=True)

st.subheader('From another angel... (with diffusion)')
with st.spinner("Generating Mooooooore.."):
    for i, dim in enumerate(st.columns(4)):
        temp = da[i]
        temp.embedding = doc.embedding
        dim.image(temp.post(f'{server_url}', parameters={'skip_rate': 0.3, 'num_images': 1}, target_executor='diffusion').matches[0].uri)