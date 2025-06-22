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

df_seoul = df[df['시도'] == '서울'].copy()

#=================== 구별 위경도 사전 ======================
gu_latlon = {
    '강남구': [37.5172, 127.0473],
    '강동구': [37.5301, 127.1238],
    '강북구': [37.6396, 127.0257],
    '강서구': [37.5509, 126.8495],
    '관악구': [37.4781, 126.9516],
    '광진구': [37.5384, 127.0823],
    '구로구': [37.4955, 126.8876],
    '금천구': [37.4569, 126.8957],
    '노원구': [37.6543, 127.0568],
    '도봉구': [37.6688, 127.0470],
    '동대문구': [37.5744, 127.0396],
    '동작구': [37.5124, 126.9392],
    '마포구': [37.5638, 126.9084],
    '서대문구': [37.5791, 126.9368],
    '서초구': [37.4837, 127.0324],
    '성동구': [37.5633, 127.0364],
    '성북구': [37.5894, 127.0167],
    '송파구': [37.5146, 127.1056],
    '양천구': [37.5170, 126.8666],
    '영등포구': [37.5264, 126.8963],
    '용산구': [37.5323, 126.9907],
    '은평구': [37.6176, 126.9227],
    '종로구': [37.5732, 126.9792],
    '중구': [37.5636, 126.9970],
    '중랑구': [37.6063, 127.0927]
}

# 구별로 위경도 컬럼 추가
df_seoul['위도'] = df_seoul['시군구'].map(lambda x: gu_latlon.get(x, [None, None])[0])
df_seoul['경도'] = df_seoul['시군구'].map(lambda x: gu_latlon.get(x, [None, None])[1])

st.subheader("서울 데이터 미리보기")
st.dataframe(df_seoul, width=1000)

st.subheader("서울시 지도")
seoul_center = [37.5665, 126.9780]
m = folium.Map(location=seoul_center, zoom_start=11)

def get_color(rate):
    if pd.isnull(rate):
        return 'gray'
    try:
        rate = float(rate)
    except:
        return 'gray'
    if rate >= 80:
        return 'green'
    elif rate >= 60:
        return 'orange'
    else:
        return 'red'

# 지도에 CircleMarker 표시
for idx, row in df_seoul.iterrows():
    if pd.notnull(row['위도']) and pd.notnull(row['경도']) and pd.notnull(row['진학율']):
        folium.CircleMarker(
            location=[row['위도'], row['경도']],
            radius=10,
            color=get_color(row['진학율']),
            fill=True,
            fill_opacity=0.75,
            popup=f"<b>{row['구']}</b><br>진학율: {row['진학율']}%",
            tooltip=row['구']
        ).add_to(m)

st_folium(m, width=1000, height=500)
