import streamlit as st
import pandas as pd
import folium
import requests
from streamlit_folium import folium_static

# 제목
st.title("서울시 진학률 지도 시각화")

# CSV 파일 업로드
uploaded_file = st.file_uploader("growup.csv", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # 데이터 확인
    st.subheader("업로드된 데이터 미리보기")
    st.dataframe(df.head())

    # 구 이름 열 확인
    if '자치구' not in df.columns:
        st.error("'자치구' 열이 필요합니다. 구 이름이 포함된 열의 이름을 '자치구'로 바꿔주세요.")
    else:
        # 진학률 열 찾기
        진학률_열 = [col for col in df.columns if '진학' in col]
        if not 진학률_열:
            st.error("진학률 데이터가 포함된 열 이름에 '진학'이라는 단어가 있어야 합니다.")
        else:
            진학률_열 = 진학률_열[0]  # 첫 번째 해당 열 사용
            df = df[['자치구', 진학률_열]].copy()
            df.columns = ['자치구', '진학률']

            # 자치구 이름 정리
            df['자치구'] = df['자치구'].str.replace(" ", "").str.replace("구", "")

            # 서울시 GeoJSON 불러오기
            geo_url = "https://raw.githubusercontent.com/southkorea/seoul-maps/master/korea/seoul/seoul_municipalities_geo_simple.json"
            geo_json = requests.get(geo_url).json()

            # 지도 생성
            m = folium.Map(location=[37.5665, 126.9780], zoom_start=11)

            folium.Choropleth(
                geo_data=geo_json,
                name="choropleth",
                data=df,
                columns=["자치구", "진학률"],
                key_on="feature.properties.name",
                fill_color="YlGnBu",
                fill_opacity=0.7,
                line_opacity=0.2,
                legend_name="서울시 진학률 (%)"
            ).add_to(m)

            st.subheader("서울시 진학률 지도")
            folium_static(m)
