import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

# 제목
st.title("서울시 시군구별 진학률 시각화")

# GitHub Raw CSV 파일 URL
url = "https://raw.githubusercontent.com/jwentertainer/project_20250621/main/growup.csv"

# CSV 불러오기
try:
    df = pd.read_csv(url)
except Exception as e:
    st.error(f"CSV 파일을 불러오는 중 오류 발생: {e}")
    st.stop()

# '서울' 시도만 필터링
seoul_df = df[df['시도'] == '서울'].copy()

# 필수 컬럼 확인
required_columns = ['시군구', '진학률', '위도', '경도']
if not all(col in seoul_df.columns for col in required_columns):
    st.error(f"CSV에 다음 컬럼이 필요합니다: {required_columns}")
    st.write("현재 포함된 컬럼:", list(df.columns))
else:
    # 서울 지도 초기화
    seoul_map = folium.Map(location=[37.5665, 126.9780], zoom_start=11)
    marker_cluster = MarkerCluster().add_to(seoul_map)

    # 각 시군구에 CircleMarker 추가
    for _, row in seoul_df.iterrows():
        folium.CircleMarker(
            location=[row['위도'], row['경도']],
            radius=row['진학률'] / 2,
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.6,
            popup=f"{row['시군구']}: {row['진학률']}%"
        ).add_to(marker_cluster)

    # 지도 출력
    folium_static(seoul_map)
