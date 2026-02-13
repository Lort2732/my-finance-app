import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# --- НАСТРОЙКА ФОНА И СТИЛЕЙ ---
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://images.unsplash.com/photo-1514924013411-cbf25faa35bb?q=80&w=2000&auto=format&fit=crop");
             background-attachment: fixed;
             background-size: cover;
         }}
         [data-testid="stVerticalBlock"] > div:has(div.stMetric) {{
             background: rgba(255, 255, 255, 0.85);
             padding: 20px;
             border-radius: 15px;
         }}
         [data-testid="stSidebar"] {{
             background-color: rgba(255, 255, 255, 0.9);
         }}
         h1, h2, h3 {{
             color: #1E1E1E;
             background: rgba(255, 255, 255, 0.7);
             padding: 10px;
             border-radius: 10px;
             display: inline-block;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

st.set_page_config(page_title="City Budget Tracker", page_icon="🏙️", layout="wide")
add_bg_from_url()

# --- ЛОГИКА ПОЛЬЗОВАТЕЛЕЙ ---
USER_DB = "users_credentials.csv"

def load_users():
    if os.path.exists(USER_DB):
        return pd.read_csv(USER_DB).to_dict('records')
    return []

def save_user(login, password):
    users = load_users()
    if any(u['login'] == login for u in users): return False
    users.append({'login': login, 'password': password})
    pd.DataFrame(users).to_csv(USER_DB, index=False)
    return True

def check_login(login, password):
    users = load_users()
    return any(u['login'] == login and str(u['password']) == str(password) for u in users)

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_login = None

# --- ЭКРАН ВХОДА ---
if not st.session_state.authenticated:
    st.title("🏙️ Мій Бюджет у Великому Місті")
    tab1, tab2 = st.tabs(["🔑 Вхід", "📝 Реєстрація"])
    with tab1:
        with st.form("login_form"):
            l_login = st.text_input("Логін").strip().lower()
            l_pass = st.text_input("Пароль", type="password")
            if st.form_submit_button("Увійти"):
                if check_login(l_login, l_pass):
                    st.session_state.authenticated = True
                    st.session_state.user_login = l_login
                    st.rerun()
                else: st.error("Помилка входу")
    with tab2:
        with st.form("reg_form"):
            r_login = st.text_input("Новий логін").strip().lower()
            r_pass = st.text_input("Новий пароль", type="password")
            if st.form_submit_button("Створити кабінет"):
                if r_login and r_pass:
                    if save_user(r_login, r_pass): st.success("Готово! Тепер увійдіть.")
                    else: st.error("Логін зайнятий")
    st.stop()

# --- ДАННЫЕ И ИНТЕРФЕЙС ---
USER_FILE = f"expenses_{st.session_state.user_login}.csv"
if 'df' not in st.session_state:
    if os.path.exists(USER_FILE):
        st.session_state.df = pd.read_csv(USER_FILE, encoding='utf-8-sig')
    else:
        st.session_state.df = pd.DataFrame(columns=["Дата", "Назва", "Сума", "Категорія"])

st.sidebar.markdown(f"### 👤 {st.session_state.user_login.capitalize()}")
if st.sidebar.button("Вийти"):
    st.session_state.authenticated = False
    st.rerun()

st.title(f"📊 Витрати: {st.session_state.user_login.capitalize()}")

with st.sidebar:
    with st.form("add_exp", clear_on_submit=True):
        st.write("🛒 **Додати покупку**")
        item = st.text_input("Що купили?")
        price = st.number_input("Сума (грн)", min_value=0.0)
        cat = st.selectbox("Категорія", ["🍏 Продукти", "🚕 Транспорт", "🏠 Житло", "💊 Аптека", "🎭 Розваги", "📱 Зв'язок", "🎁 Інше"])
        if st.form_submit_button("Додати"):
            new_row = pd.DataFrame({"Дата": [datetime.now().strftime("%d.%m.%Y")], "Назва": [item], "Сума": [price], "Категорія": [cat]})
            st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
            st.session_state.df.to_csv(USER_FILE, index=False, encoding='utf-8-sig')
            st.rerun()

df = st.session_state.df
if not df.empty:
    st.metric("Загальний підсумок", f"{df['Сума'].sum():,.2f} грн")
    c1, c2 = st.columns([1.5, 1])
    with c1: st.dataframe(df, use_container_width=True, hide_index=True)
    with c2:
        fig = px.pie(df, values='Сума', names='Категорія', hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Поки що порожньо.")
