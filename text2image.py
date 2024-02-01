import streamlit as st
from sd import generate

st.set_page_config(
    page_title='t2i'
)

st.header("그림 그려줌", divider="rainbow")

content = st.text_input("그리고 싶은 것(영어로)")
button = st.button("그리기")

if button:
    with st.spinner('그림 그리는중...'):
        result = generate(content)
    st.image(result)
    st.success('완료')