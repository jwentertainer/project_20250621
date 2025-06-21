import streamlit as st
import pandas as pd
import folium
import requests
from streamlit_folium import folium_static

st.title("서울시 진학률 지도 시각화")

def show_error(msg): st.error(msg)

@st.cache_data
def load_data():
    return pd.read_csv("growup.csv", encoding="cp949")

uploaded = st.file_uploader("CSV 파일 선택", type="csv")
try:
    if uploaded:
        df = pd.read_csv(uploaded, encoding="cp949")
    else:
        df = load_data()
except UnicodeDecodeError:
    show_error("파일 인코딩 문제! 'CSV 파일 저장' 시 'ANSI(또는 cp949)'로 인코딩했는지 확인하세요. 그래도 안 되면 utf-8로 저장/업로드해보세요.")
    st.stop()

st.subheader("CSV 데이터 미리보기")
st.dataframe(df.head())

if '자치구' not in df.columns:
    show_error("'자치구' 열이 없습니다.")
    st.stop()

진학열 = [col for col in df.columns if '진학' in col]
if not 진학열:
    show_error("진학률 컬럼이 없습니다.")
    st.stop()

진학열 = 진학열[0]
df = df[['자치구', 진학열]].copy()
df.columns = ['자치구', '진학률']

df['자치구'] = df['자치구'].str.strip().str.replace(" ", "")
geo_url = "https://raw.githubusercontent.com/southkorea/seoul-maps/master/korea/seoul/seoul_municipalities_geo_simple.json"
geo_json = requests.get(geo_url).json()

key_names = [f['properties']['name'] for f in geo_json['features']]
if not set(df['자치구']).issubset(set(key_names)):
    st.warning(f"자치구명 불일치:\nDataframe:{df['자치구'].unique()}\nGeojson:{key_names}")

m = folium.Map(location=[37.5665, 126.9780], zoom_start=11)
folium.Choropleth(
    geo_data=geo_json, name="choropleth",
    data=df, columns=["자치구", "진학률"],
    key_on="feature.properties.name",
    fill_color="YlGnBu",
    fill_opacity=0.7, line_opacity=0.2,
    legend_name="서울시 진학률 (%)"
).add_to(m)
st.subheader("서울시 진학률 지도")
folium_static(m)
