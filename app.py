import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# --- НАСТРОЙКА НОЧНОГО ФОНА И ТЕМНОГО СТИЛЯ ---
def add_dark_city_theme():
    st.markdown(
         f"""
         <style>
         /* Фоновое изображение ночного города */
         .stApp {{
             background-image: url("https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?q=80&w=2000&auto=format&fit=crop");
             background-attachment: fixed;
             background-size: cover;
         }}

         /* Делаем блоки контента темными и читабельными */
         [data-testid="stVerticalBlock"] > div:has(div.stMetric), .stTabs {{
             background: rgba(20, 20, 20, 0.85);
             padding: 25px;
             border-radius: 15px;
             border: 1px solid #444;
             color: white;
         }}
         
         /* Темная боковая панель */
         [data-testid="stSidebar"] {{
             background-color: rgba(10, 10, 10, 0.95);
             color: white;
         }}

         /* Весь текст делаем белым */
         h1, h2, h3, p, span, label, .stMarkdown {{
             color: white !important;
         }}

         /* Стиль для таблиц (черный фон) */
         .stDataFrame {{
             background: rgba(0, 0, 0, 0.5);
             border-radius: 10px;
         }}

         /* Настройка кнопок, чтобы они выделялись */
         .stButton>button {{
             background-color: #007bff;
             color: white;
             border-radius: 8px;
             width: 100%;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

st.set_page_config(page_title="Night City Budget", page_icon="🌃", layout="wide")
add_dark_city_theme()

# --- ЛОГИКА ПОЛЬЗОВАТЕЛЕЙ (CSV база) ---
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

# --- ЭКРАН ВХОДА (ТЕМНЫЙ) ---
if not st.session_state.authenticated:
    st.title("🌃 Мій Нічний Бюджет")
    tab1, tab2 = st.tabs(["🔐 Вхід", "📝 Реєстрація"])
    with tab1:
        with st.form("login_form"):
            l_login = st.text_input("Логін").strip().lower()
            l_pass = st.text_input("Пароль", type="password")
            if st.form_submit_button("Увійти"):
                if check_login(l_login, l_pass):
                    st.session_state.authenticated = True
                    st.session_state.user_login = l_login
                    st.rerun()
                else: st.error("Помилка входу. Спробуйте ще раз.")
    with tab2:
        with st.form("reg_form"):
            r_login = st.text_input("Вигадайте логін").strip().lower()
            r_pass = st.text_input("Вигадайте пароль", type="password")
            if st.form_submit_button("Створити кабінет"):
                if r_login and r_pass:
                    if save_user(r_login, r_pass): st.success("Готово! Тепер можна увійти.")
                    else: st.error("Логін вже зайнятий")
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

st.title(f"🌃 Витрати міста: {st.session_state.user_login.capitalize()}")

with st.sidebar:
    with st.form("add_exp", clear_on_submit=True):
        st.write("🛒 **Нова операція**")
        item = st.text_input("Назва (магазин/товар)")
        price = st.number_input("Сума (грн)", min_value=0.0)
        cat = st.selectbox("Категорія", ["🍏 Продукти", "🚕 Транспорт", "🏠 Житло", "💊 Аптека", "🎭 Розваги", "🎁 Інше"])
        if st.form_submit_button("Додати до списку"):
            new_row = pd.DataFrame({"Дата": [datetime.now().strftime("%d.%m.%Y")], "Назва": [item], "Сума": [price], "Категорія": [cat]})
            st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
            st.session_state.df.to_csv(USER_FILE, index=False, encoding='utf-8-sig')
            st.rerun()

# Основной контент
df = st.session_state.df
if not df.empty:
    st.metric("Витрачено за весь час", f"{df['Сума'].sum():,.2f} грн")
    c1, c2 = st.columns([1.5, 1])
    with c1:
        st.markdown("### 📋 Історія операцій")
        st.dataframe(df, use_container_width=True, hide_index=True)
    with c2:
        st.markdown("### 📊 Структура")
        fig = px.pie(df, values='Сума', names='Категорія', hole=0.4, 
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Ваш нічний кабінет порожній. Додайте перші дані через бокове меню.")
