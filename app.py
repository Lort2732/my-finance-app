import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# 1. СТИЛЬ ПРИЛОЖЕНИЯ
def apply_style():
    st.markdown("""
        <style>
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?q=80&w=2000&auto=format&fit=crop");
            background-attachment: fixed;
            background-size: cover;
        }
        [data-testid="stVerticalBlock"] > div:has(div.stMetric), .stTabs, .stExpander {
            background: rgba(15, 15, 15, 0.8) !important;
            backdrop-filter: blur(15px);
            border-radius: 20px !important;
            border: 1px solid rgba(0, 255, 136, 0.3);
            padding: 20px !important;
        }
        [data-testid="stSidebar"] {
            background-color: rgba(0, 0, 0, 0.9) !important;
        }
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

st.set_page_config(page_title="Finance Neon", layout="wide")
apply_style()

# 2. БАЗА ПОЛЬЗОВАТЕЛЕЙ
USER_DB = "users_credentials.csv"
def get_users():
    return pd.read_csv(USER_DB).to_dict('records') if os.path.exists(USER_DB) else []

def save_user(login, password):
    users = get_users()
    if any(u['login'] == login for u in users): return False
    users.append({'login': login, 'password': password})
    pd.DataFrame(users).to_csv(USER_DB, index=False)
    return True

if 'auth' not in st.session_state:
    st.session_state.auth = False
    st.session_state.user = None

# 3. ЭКРАН ВХОДА
if not st.session_state.auth:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<h1 style='text-align: center;'>🏙️ FINANCE PRO</h1>", unsafe_allow_html=True)
        t = st.tabs(["🔐 ВХІД", "📝 РЕЄСТРАЦІЯ"])
        with t[0]:
            with st.form("l"):
                u = st.text_input("Логін").lower().strip()
                p = st.text_input("Пароль", type="password")
                if st.form_submit_button("УВІЙТИ"):
                    if any(x['login'] == u and str(x['password']) == str(p) for x in get_users()):
                        st.session_state.auth, st.session_state.user = True, u
                        st.rerun()
                    else: st.error("Помилка")
        with t[1]:
            with st.form("r"):
                ru, rp = st.text_input("Логін"), st.text_input("Пароль", type="password")
                if st.form_submit_button("СТВОРИТИ"):
