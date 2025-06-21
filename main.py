import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static

# Streamlit 타이틀
st.title("서울시 진학률 시각화")

# GitHub CSV 파일 경로 (아래는 예시입니다. 본인의 실제 raw GitHub URL로 대체하세요)
csv_url = "https://raw.githubusercontent.com/jwentertainer/project_20250621/blob/main/growup.csv"

# 서울시 GeoJSON (자치구 경계)
geo_url = "https://raw.githubusercontent.com/southkorea/seoul-maps/master/korea/seoul/seoul_municipalities_geo_simple.json"

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv(csv_url)
    geo = gpd.read_file(geo_url)
    return df, geo

df, geo = load_data()

# 데이터 확인
st.subheader("원본 데이터 (상위 5개 행)")
st.write(df.head())

# 서울시 자치구 이름 리스트 (GeoJSON 기준)
geo['name'] = geo['name'].str.replace(' ', '').str.replace('구', '')
seoul_districts = geo['name'].tolist()

# 자치구 열과 진학률 열 찾기
구_열 = None
진학률_열 = None
for col in df.columns:
    if '구' in col or '지역' in col or '자치구' in col:
        구_열 = col
    if '진학' in col:
        진학률_열 = col

if 구_열 is None or 진학률_열 is None:
    st.error("CSV 파일에서 '구' 또는 '진학률' 정보를 찾을 수 없습니다.")
else:
    # 필터링: 서울시 자치구만 선택
    df[구_열] = df[구_열].str.replace(' ', '').str.replace('구', '')
    df_filtered = df[df[구_열].isin(seoul_districts)][[구_열, 진학률_열]].copy()
    df_filtered.columns = ['자치구', '진학률']

    # 병합
    merged = geo.merge(df_filtered, left_on='name', right_on='자치구')

    # Folium 지도 생성
    m = folium.Map(location=[37.5665, 126.9780], zoom_start=11)

    folium.Choropleth(
        geo_data=merged,
        data=merged,
        columns=['name', '진학률'],
        key_on='feature.properties.name',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='서울시 진학률 (%)',
    ).add_to(m)

    # 팝업 추가
    for _, row in merged.iterrows():
        folium.Marker(
            location=[row.geometry.centroid.y, row.geometry.centroid.x],
            popup=f"{row['name']}구: {row['진학률']}%"
        ).add_to(m)

    st.subheader("서울시 진학률 지도")
    folium_static(m)
