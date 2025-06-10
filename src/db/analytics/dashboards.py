"""
dashboards.py

Streamlit dashboard skeleton.
"""

import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Baseball Frame Analytics", layout="wide")

st.title("Baseball Frame Analytics Dashboard")

api_url = st.text_input("API Endpoint", "http://localhost:8000/recent_frames")
if st.button("Load Data"):
    resp = requests.get(api_url)
    if resp.ok:
        data = resp.json()
        df = pd.DataFrame(data)
        st.dataframe(df)
    else:
        st.error(f"Failed to fetch data: {resp.status_code}")
