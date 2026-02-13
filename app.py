import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# 1. Оформление интерфейса (Neon Green & Dark Mode) 🎨
def apply_style():
    st.markdown("""
        <style>
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?q=80&w=2000&auto=format&fit=crop");
            background-attachment: fixed;
            background-size: cover;
        }
        [data-testid="stVerticalBlock"] > div:has(div.stMetric), .stTabs, .stExpander {
            background: rgba(15, 15, 15, 0.85) !important;
            backdrop-filter: blur(15px);
            border-radius: 20px !important;
            border: 1px solid rgba(0, 255, 136, 0.3);
            padding: 20px !important;
        }
        [data-testid="stSidebar"] { background-color: rgba(0, 0, 0, 0.9) !important; }
        h1, h2, h3, p, span, label, .stMarkdown { color: white !important; }
        .stButton>button {
            background: linear-gradient(135deg, #00ff88 0%, #00a86b 100%) !important;
            color: black !important;
            border-radius: 12px !important;
            font-weight: bold !important;
            height: 45px;
            width: 100%;
        }
        [data-testid="stMetricValue"] {
            color: #00ff88 !important;
            text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
        }
        </style>
        """, unsafe_allow_html=True)

st.set_page_config(page_title="Finance Neon Pro", layout="wide")
apply_style()

# 2. Логика пользователей 🔐
USER_DB = "users_credentials.csv"
def get_users():
    if os.path.exists(USER_DB):
        return pd.read_csv(USER_DB).to_dict('records')
    return []

def save_user(login, password):
    users = get_users()
    if any(u['login'] == login for u in users):
        return False
    users.append({'login': login, 'password': password})
    pd.DataFrame(users).to_csv(USER_DB, index=False)
    return True

if 'auth' not in st.session_state:
    st.session_state.auth
