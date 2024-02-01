import streamlit as st
from streamlit_drawable_canvas import st_canvas
from sd import generate, generate_i2i
from PIL import Image

st.set_page_config(
    page_title='i2i'
)

st.header("그림 그려줌", divider="rainbow")

# 색상 선택기
stroke_color = st.color_picker("선 색상 선택", '#000000')

# 그림 그리기 캔버스 만들기
canvas_result = st_canvas(
    fill_color="rgba(0, 0, 0, 0)",  # 채우기 색상
    stroke_width=2,  # 선의 너비
    stroke_color=stroke_color,  # 사용자가 선택한 선의 색상
    background_color="#ffffff",  # 배경색
    height=500,  # 캔버스의 높이
    width=600,  # 캔버스의 너비
    drawing_mode="freedraw",  # 그리기 모드
    key="canvas",
)

button = st.button("그림 제출")

if button:
    with st.spinner('그림 그리는중...'):
        image = Image.fromarray(canvas_result.image_data)
        image = image.convert("RGB")
        result = generate_i2i(prompt='', image=image)
    st.image(result)
    st.success('완료')