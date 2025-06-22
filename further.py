import streamlit as st
import pandas as pd

st.title("growup.csv 데이터 표 시각화")

# 깃허브 raw csv 파일 URL
csv_url = "https://raw.githubusercontent.com/jwentertainer/project_20250621/main/growup.csv"

# CSV 파일 읽기
df = pd.read_csv(csv_url)

# 표 출력
st.subheader("데이터 미리보기")
st.dataframe(df)
