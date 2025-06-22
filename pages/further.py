# import streamlit as st
# import pandas as pd
# import folium
# from streamlit_folium import st_folium

# st.title("지도로 진학률 보기")

# # 깃허브 raw csv 파일 URL
# csv_url = "https://raw.githubusercontent.com/jwentertainer/project_20250621/main/growup.csv"

# # CSV 파일 읽기
# df = pd.read_csv(csv_url)

# # '시도'가 '서울'인 데이터만 필터링
# df_seoul = df[df['시도'] == '서울']

# # 표 출력
# st.subheader("서울 데이터 미리보기")
# st.dataframe(df_seoul, width=1000) # 표 가로 크기 지정

# # folium 지도 준비
# st.subheader("서울시 지도")
# seoul_center = [37.5665, 126.9780] # 서울시청 위도, 경도

# m = folium.Map(location=seoul_center, zoom_start=11)

# st_folium(m, width=1000, height=500) # 지도 가로 크기 맞춤


import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.title("지도로 진학률 보기")

csv_url = "https://raw.githubusercontent.com/jwentertainer/project_20250621/main/growup.csv"
df = pd.read_csv(csv_url)

df_seoul = df[df['시도'] == '서울']
st.subheader("서울 데이터 미리보기")
st.dataframe(df_seoul, width=1000)

st.subheader("서울시 지도")
seoul_center = [37.5665, 126.9780]
m = folium.Map(location=seoul_center, zoom_start=11)

# 진학율에 따라 색상, 반경 조절
def get_color(rate):
    if rate >= 80:
        return 'green'
    elif rate >= 60:
        return 'orange'
    else:
        return 'red'

for idx, row in df_seoul.iterrows():
    if pd.notnull(row['위도']) and pd.notnull(row['경도']) and pd.notnull(row['진학율']):
        folium.CircleMarker(
            location=[row['위도'], row['경도']],
            radius=8,
            color=get_color(row['진학율']),
            fill=True,
            fill_opacity=0.7,
            popup=f"<b>{row['학교명']}</b><br>진학율: {row['진학율']}%",
            tooltip=row['학교명']
        ).add_to(m)

st_folium(m, width=1000, height=500)
