import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# 1. ГЛАВНЫЙ СТИЛЬ (NEON GREEN)
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

st.set_page_config(page_title="Finance Neon", layout="wide")
apply_style()

# 2. РАБОТА С ЮЗЕРАМИ
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
    st.session_state.auth = False
    st.session_state.user = None

# 3. ЛОГИН И РЕГИСТРАЦИЯ
if not st.session_state.auth:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<h1 style='text-align: center;'>🏙️ FINANCE PRO</h1>", unsafe_allow_html=True)
        t = st.tabs(["🔐 ВХІД", "📝 РЕЄСТРАЦІЯ"])
        with t[0]:
            with st.form("login"):
                u = st.text_input("Логін").lower().strip()
                p = st.text_input("Пароль", type="password")
                if st.form_submit_button("УВІЙТИ"):
                    if any(x['login'] == u and str(x['password']) == str(p) for x in get_users()):
                        st.session_state.auth = True
                        st.session_state.user = u
                        st.rerun()
                    else:
                        st.error("Помилка")
        with t[1]:
            with st.form("reg"):
                ru = st.text_input("Логін")
                rp = st.text_input("Пароль", type="password")
                if st.form_submit_button("СТВОРИТИ"):
                    if ru and rp:
                        if save_user(ru.lower().strip(), rp):
                            st.success("ОК! Можна входити.")
                        else:
                            st.error("Логін зайнятий")
                    else:
                        st.warning("Заповніть поля")
    st.stop()

# 4. ДАННЫЕ И ИНТЕРФЕЙС
FILE = f"expenses_{st.session_state.user}.csv"
if 'df' not in st.session_state:
    if os.path.exists(FILE):
        st.session_state.df = pd.read_csv(FILE)
    else:
        st.session_state.df = pd.DataFrame(columns=["Дата", "Назва", "Сума", "Категорія"])

with st.sidebar:
    st.title(f"👤 {st.session_state.user}")
    if st.button("ВИЙТИ"):
        st.session_state.auth = False
        st.rerun()
    with st.form("add"):
        name = st.text_input("Назва")
        price = st.number_input("Сума", min_value=0.0)
        cat = st.selectbox("Категорія", ["🍏 Продукти", "🚕 Транспорт", "🏠 Житло", "💊 Аптека", "🎭 Розваги", "🎁 Інше"])
        if st.form_submit_button("ДОДАТИ"):
            new = pd.DataFrame({"Дата": [datetime.now().strftime("%d.%m.%Y")], "Назва": [name], "Сума": [price], "Категорія": [cat]})
            st.session_state.df = pd.concat([st.session_state.df, new], ignore_index=True)
            st.session_state.df.to_csv(FILE, index=False)
            st.rerun()

st.title("🚀 ДЕШБОРД ВИТРАТ")
df = st.session_state.df
if not df.empty:
    st.metric("РАЗОМ", f"{df['Сума'].sum()} ₴")
    c1, c2 = st.columns([1.5, 1])
    with c1:
        st.dataframe(df, use_container_width=True)
        idx = st.selectbox("Обрати рядок", df.index)
        col_edit, col_del = st.columns(2)
        with col_edit:
            with st.popover("📝 ЗМІНИТИ"):
                en = st.text_input("Нова назва", value=df.at[idx, 'Назва'])
                ep = st.number_input("Нова сума", value=float(df.at[idx, 'Сума']))
                if st.button("ЗБЕРЕГТИ"):
                    st.session_state.df.at[idx, 'Назва'] = en
                    st.session_state.df.at[idx, 'Сума'] = ep
                    st.session_state.df.to_csv(FILE, index=False)
                    st.rerun()
        with col_del:
            if st.button("🗑️ ВИДАЛИТИ"):
                st.session_state.df = st.session_state.df.drop(idx).reset_index(drop=True)
                st.session
