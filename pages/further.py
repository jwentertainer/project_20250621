import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 여백 제거용 CSS 추가
st.markdown("""
    <style>
    /* 전체 섹션 여백과 패딩 없애기 */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 0rem;
        padding-right: 0rem;
        margin: 0;
    }
    .element-container {
        padding: 0 !important;
        margin: 0 !important;
    }
    /* folium map이 들어가는 div 여백 제거 */
    div.st_folium {
        padding: 0 !important;
        margin: 0 !important;
    }
    /* 전체 배경도 흰색으로 강제 (선택사항) */
    .stApp {
        background-color: #fff !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("지도로 진학률 보기")

# 깃허브 raw csv 파일 URL
csv_url = "https://raw.githubusercontent.com/jwentertainer/project_20250621/main/growup.csv"

# CSV 파일 읽기
df = pd.read_csv(csv_url)

# '시도'가 '서울'인 데이터만 필터링
df_seoul = df[df['시도'] == '서울']

# 표 출력
st.subheader("서울 데이터 미리보기")
st.dataframe(df_seoul, width=1000)

# folium 지도 준비
st.subheader("서울시 지도")
seoul_center = [37.5665, 126.9780]  # 서울시청 위도, 경도
m = folium.Map(location=seoul_center, zoom_start=11)

# 지도 출력(여백 최소화, width 지정)
st_folium(m, width=1000, height=500)
