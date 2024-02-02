import streamlit as st
from streamlit_drawable_canvas import st_canvas
from sd import generate, generate_i2i
from PIL import Image

st.set_page_config(
    page_title='i2i'
)

st.header("그림 그려줌", divider="rainbow")

content = st.text_input("그린 것 설명(영어로)(안써도됨)")



# 체크박스 추가
check = st.checkbox('사진 업로드 기능 사용')

if not check:
    # 색상 선택기
    stroke_color = st.color_picker("선 색상 선택", '#000000')

    # 선의 너비를 사용자가 선택 가능하도록 슬라이더 추가
    stroke_width = st.slider("굵기 선택", min_value=1, max_value=50, value=2)
    # 그림 그리기 캔버스 만들기
    canvas_result = st_canvas(
        fill_color="rgb(0, 0, 0)",  # 채우기 색상
        stroke_width=stroke_width,  # 선의 너비
        stroke_color=stroke_color,  # 사용자가 선택한 선의 색상
        background_color="#ffffff",  # 배경색
        height=500,  # 캔버스의 높이
        width=600,  # 캔버스의 너비
        drawing_mode="freedraw",  # 그리기 모드
        key="canvas",
    )
else:
    uploaded_file = st.file_uploader("사진 업로드", type=["jpg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)

button = st.button("그림 제출")
st.text("**********검정 그림 나오면 제출 한번 더 누르기***********")
if button:
    with st.spinner('그림 그리는중...'):
        if not check:
            image = Image.fromarray(canvas_result.image_data)
            image = image.convert("RGB")
        else:
            image = image.convert("RGB")
            image = image.resize((512, 512))
        result = generate_i2i(prompt='', image=image)
    st.image(result)
    st.success('완료')