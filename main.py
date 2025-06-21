import streamlit as st
import pandas as pd
import folium
import requests
from streamlit_folium import folium_static

# 제목
st.title("서울시 진학률 지도 시각화")

# GitHub의 raw CSV URL 입력 (★ 여기를 본인 GitHub CSV 주소로 교체하세요)
#csv_url = "https://raw.githubusercontent.com/jwentertainer/project_20250621/blob/main/growup.csv"

# CSV 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("growup.csv", encoding="cp949") #csv_url
    return df

df = load_data()

# 데이터 확인
st.subheader("CSV 데이터 미리보기")
st.dataframe(df.head())

# 구 이름 열 확인
if '시군구' not in df.columns:
    st.error("'시군구' 열이 필요합니다. 구 이름이 포함된 열의 이름을 '시군구'로 바꿔주세요.")
else:
    # 진학률 열 찾기
    진학률_열 = [col for col in df.columns if '진학' in col]
    if not 진학률_열:
        st.error("진학률 데이터가 포함된 열 이름에 '진학'이라는 단어가 있어야 합니다.")
    else:
        진학률_열 = 진학률_열[0]
        df = df[['시군구', 진학률_열]].copy()
        df.columns = ['시군구', '진학률']

        # 시군구 이름 정리
        df['시군구'] = df['시군구'].str.strip().str.replace(" ", "")

        # 서울시 GeoJSON 불러오기
        geo_url = "https://raw.githubusercontent.com/southkorea/seoul-maps/master/korea/seoul/seoul_municipalities_geo_simple.json"
        geo_json = requests.get(geo_url).json()

        # 지도 생성
        m = folium.Map(location=[37.5665, 126.9780], zoom_start=11)

        folium.Choropleth(
            geo_data=geo_json,
            name="choropleth",
            data=df,
            columns=["시군구", "진학률"],
            key_on="feature.properties.name",
            fill_color="YlGnBu",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name="서울시 진학률 (%)"
        ).add_to(m)

        st.subheader("서울시 진학률 지도")
        folium_static(m)
