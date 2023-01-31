import streamlit as st
from PIL import Image


col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    st.header("Olist's maching learning models")
    image = Image.open("src/brain.png")
    st.write("")
    st.image(image, caption="")
