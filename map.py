import streamlit as st
import folium
from streamlit_folium import folium_static

st.title("서울시 지도 예제")

# 서울시 중심 좌표
seoul_center = [37.5665, 126.9780]

# Folium 지도 생성
m = folium.Map(location=seoul_center, zoom_start=11)

# (선택) 서울시 마커 표시
folium.Marker(seoul_center, tooltip="서울특별시 중심").add_to(m)

# Streamlit에 지도 표시
folium_static(m)
