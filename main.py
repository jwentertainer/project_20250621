import streamlit as st
import folium
from streamlit_folium import folium_static
import requests

st.title("서울시 자치구별 경계선 지도")

# 서울 중심 좌표
seoul_center = [37.5665, 126.9780]

# 외부 geojson(서울시 자치구 경계) 파일 URL
geojson_url = "https://raw.githubusercontent.com/southkorea/seoul-maps/master/korea/seoul/seoul_municipalities_geo_simple.json"

# geojson 가져오기
geojson_data = requests.get(geojson_url).json()

# Folium 지도 생성
m = folium.Map(location=seoul_center, zoom_start=11)

# 경계선 표시 (자치구별)
folium.GeoJson(
    geojson_data,
    name='자치구 경계',
    style_function=lambda feature: {
        'fillOpacity': 0.0,      # 내부를 채우지 않음 (투명)
        'color': 'blue',
        'weight': 2
    },
    tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['자치구']),
).add_to(m)

# (선택) 서울시 전체 외곽선 강조
# 이미 geojson이 구별 경계와 서울시 외곽선을 모두 포함하므로, 이 과정이 별도로 필요하지는 않습니다.

# Streamlit에 지도 표시
folium_static(m)
