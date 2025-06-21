import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static

# 제목
st.title("서울시 진학률 지도 시각화")

# CSV 파일 업로드
uploaded_file = st.file_uploader("growup.csv", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # 구 이름 열 이름이 정확히 무엇인지 확인 후 수정 필요
    st.subheader("업로드된 데이터 미리보기")
    st.dataframe(df.head())

    # '지역' 혹은 '자치구' 등으로 되어 있을 가능성 있음. 예시로 '자치구'라고 가정
    if '자치구' not in df.columns:
        st.error("자치구(구 이름)를 나타내는 열이 '자치구'로 되어 있어야 합니다.")
    else:
        # 진학률 열 이름을 확인 (예: '진학률', '대학진학률' 등)
        진학률_열 = [col for col in df.columns if '진학' in col]
        if not 진학률_열:
            st.error("진학률 열을 찾을 수 없습니다. '진학'이라는 단어가 들어간 열 이름을 확인해주세요.")
        else:
            진학률_열 = 진학률_열[0]  # 첫 번째 해당 열 사용
            df = df[['자치구', 진학률_열]].copy()
            df.columns = ['자치구', '진학률']

            # 서울시 행정구 GeoJSON (공식 또는 외부 경로 사용)
            seoul_geo_url = "https://raw.githubusercontent.com/southkorea/seoul-maps/master/korea/seoul/seoul_municipalities_geo_simple.json"
            seoul_geo = gpd.read_file(seoul_geo_url)

            # 구 이름 일치 여부 확인
            df['자치구'] = df['자치구'].str.replace(' ', '').str.replace('구', '')
            seoul_geo['name'] = seoul_geo['name'].str.replace(' ', '').str.replace('구', '')

            # 병합 준비
            merged = seoul_geo.merge(df, left_on='name', right_on='자치구')

            # 중심 위치
            m = folium.Map(location=[37.5665, 126.9780], zoom_start=11)

            # Choropleth
            folium.Choropleth(
                geo_data=merged,
                data=merged,
                columns=["name", "진학률"],
                key_on="feature.properties.name",
                fill_color="YlGnBu",
                fill_opacity=0.7,
                line_opacity=0.2,
                legend_name="서울시 진학률 (%)"
            ).add_to(m)

            # 팝업
            for _, r in merged.iterrows():
                folium.Popup(f"{r['name']}구: {r['진학률']}%").add_to(
                    folium.GeoJson(r['geometry'])
                )

            st.subheader("서울시 진학률 지도")
            folium_static(m)
