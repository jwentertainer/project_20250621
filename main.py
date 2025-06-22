import streamlit as st

st.set_page_config(page_title="2024학년도 진학율", layout="centered")

st.markdown("""
    <style>
    .proj-title {
        text-align: center;
        color: #fff;
        font-size: 6em;
        font-weight: bold;
        text-shadow: 2px 2px 10px #1565c0, 0 0 10px #4fc3f7;
        margin-top: 2em;
        margin-bottom: 2em;
    }
    .stApp {
        background: linear-gradient(135deg, #2196f3 0%, #e3f2fd 100%);
    }
    </style>
    <div class='proj-title'>
        2024학년도 진학율
    </div>
""", unsafe_allow_html=True)
