import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image

# Title
image = Image.open('KDT-JU.png')

st.title("My first web app")
st.image(image)
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['a', 'b', 'c'])
st.dataframe(chart_data)
sel = st.selectbox('Select column',['a', 'b', 'c'])
st.bar_chart(chart_data[sel])

