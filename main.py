import streamlit as st
import pandas as pd

st.set_page_config(page_title="KBO 팀 WAR 순위", page_icon="⚾")

st.title("⚾ KBO 팀 WAR 순위(1982-2023)")

url = "https://statiz.sporki.com/?mid=stat&re=0&ys=1982&ye=2023&se=0&te=&tm=&ty=0&qu=auto&po=0&as=&ae=&hi=&un=&pl=&da=1&o1=WAR_ALL_ADJ&o2=TPA&de=1&tr=&cv=&ml=1&sn=30&pa=0&si=&cn=&lr=1"

# 페이지의 모든 테이블 읽기
tables = pd.read_html(url)

# 일반적으로 첫번째(혹은 두번째) 테이블에 팀 순위가 들어갑니다.
# 출력해서 확인:
st.write("테이블 미리보기")
for i, df in enumerate(tables):
    st.write(f"Table {i}")
    st.dataframe(df)

# 실제 팀 순위 테이블 선택(예시상 1번째 또는 0번째 예상)
team_rank_df = tables[0]

# 컬럼명/데이터 확인하여 불필요한 컬럼/로우 제거(필요시)
# team_rank_df = team_rank_df.dropna(subset=['팀']).reset_index(drop=True)

st.subheader("팀 순위")
st.dataframe(team_rank_df)

# 예시: 컬럼이 ['순', '팀', 'WAR_ALL_ADJ', ...] 라고 가정
if 'WAR_ALL_ADJ' in team_rank_df.columns:
    st.bar_chart(team_rank_df.set_index('팀')['WAR_ALL_ADJ'])

st.caption(f"출처: [STATIZ]({url})")
