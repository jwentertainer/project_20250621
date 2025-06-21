import streamlit as st
import folium
import json
from streamlit_folium import st_folium

st.set_page_config(layout="wide")
st.title("서울시 및 자치구 행정경계 지도(geopandas 미사용)")

# 1. GeoJSON 파일 불러오기
geojson_path = "seoul_gu.geojson"  # 같은 폴더에 있다고 가정
with open(geojson_path, encoding="utf-8") as f:
    data = json.load(f)

# 2. 지도 중심 및 기본 생성
center = [37.5665, 126.9780]  # 서울시청 좌표
m = folium.Map(location=center, zoom_start=11)

# 3. 자치구 경계 표시
for feature in data["features"]:
    gu_name = feature["properties"].get("NAME", feature["properties"].get("EMD_KOR_NM", ""))
    folium.GeoJson(
        feature["geometry"],
        name=gu_name,
        style_function=lambda x: {
            "color": "red",
            "weight": 2,
            "fillOpacity": 0.07,
        },
        highlight_function=lambda x: {"weight": 4, "color": "blue"},
        tooltip=gu_name,
    ).add_to(m)

# 4. 레이어 컨트롤 (선택적)
folium.LayerControl().add_to(m)

# 5. 지도 출력
st_folium(m, width=1000, height=700)
