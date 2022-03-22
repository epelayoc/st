import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image

@st.cache      # IMPORTANT: Cache the conversion to prevent computation on every rerun
def gen_df():
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['a', 'b', 'c'])
    return chart_data

image = Image.open('KDT-JU.png')
st.image(image)
st.title("Partner search tool")

df = gen_df()
st.dataframe(df)
sel = st.selectbox('Select country',['Spain', 'France', 'Germany'])
st.bar_chart(df[sel])



