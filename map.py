import streamlit as st
import folium
from streamlit_folium import st_folium

st.title("서울시 지도 보기")

# 서울시 중심 좌표 (서울 시청 인근)
seoul_lat, seoul_lon = 37.5665, 126.9780

# Folium 지도 만들기
m = folium.Map(location=[seoul_lat, seoul_lon], zoom_start=11)

# 지도 출력
st_folium(m, width=700, height=500)
