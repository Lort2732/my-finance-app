import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# --- НАСТРОЙКА ТЕМЫ ---
def add_dark_city_theme():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?q=80&w=2000&auto=format&fit=crop");
             background-attachment: fixed;
             background-size: cover;
         }}
         [data-testid="stVerticalBlock"] > div:has(div.stMetric), .stTabs {{
             background: rgba(20, 20, 20, 0.85);
             padding: 25px;
             border-radius: 15px;
             border: 1px solid #444;
             color: white;
         }}
         [data-testid="stSidebar"] {{
             background-color: rgba(10, 10, 10, 0.95);
             color: white;
         }}
         h1, h2, h3, p, span, label, .stMarkdown {{
             color: white !important;
         }}
         .stDataFrame {{
             background: rgba(0, 0, 0, 0.5);
             border-radius: 10px;
         }}
         .stButton>button {{
             background-color: #007bff;
             color: white;
             border-radius: 8px;
             width: 100%;
         }}
         .stButton>button:hover {{
             background-color: #0056b3;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

st.set_page_config(page_title="City Budget Pro", page_icon="🌃", layout="wide")
add_dark_city_theme()

# --- ЛОГИКА ПОЛЬЗОВАТЕЛЕЙ ---
USER_DB = "users_credentials.csv"

def load_users():
    if os.path.exists(USER_DB): return pd.read_csv(USER_DB).to_dict('records')
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

if not st.session_state.authenticated:
    st.title("🌃 Мій Бюджет")
    t1, t2 = st.tabs(["🔐 Вхід", "📝 Реєстрація"])
    with t1:
        with st.form("l_form"):
            l_login = st.text_input("Логін").strip().lower()
            l_pass = st.text_input("Пароль", type="password")
            if st.form_submit_button("Увійти"):
                if check_login(l_login, l_pass):
                    st.session_state.authenticated = True
                    st.session_state.user_login = l_login
                    st.rerun()
                else: st.error("Помилка входу")
    with t2:
        with st.form("r_form"):
            r_login = st.text_input("Логін")
            r_pass = st.text_input("Пароль", type="password")
            if st.form_submit_button("Створити"):
                if r_login and r_pass:
                    if save_user(r_login.strip().lower(), r_pass): st.success("Створено!")
                    else: st.error("Зайнято")
    st.stop()

# --- ДАННЫЕ ---
USER_FILE = f"expenses_{st.session_state.user_login}.csv"
def load_data():
    if os.path.exists(USER_FILE):
        return pd.read_csv(USER_FILE, encoding='utf-8-sig')
    return pd.DataFrame(columns=["Дата", "Назва", "Сума", "Категорія"])

if 'df' not in st.session_state:
    st.session_state.df = load_data()

# --- ИНТЕРФЕЙС ---
st.sidebar.markdown(f"### 👤 {st.session_state.user_login.capitalize()}")
if st.sidebar.button("Вийти"):
    st.session_state.authenticated = False
    st.rerun()

st.title(f"🌃 Керування бюджетом: {st.session_state.user_login.capitalize()}")

# Блок добавления
with st.sidebar:
    st.header("➕ Додати нову")
    with st.form("add_form", clear_on_submit=True):
        item = st.text_input("Назва")
        price = st.number_input("Сума", min_value=0.0)
        cat = st.selectbox("Категорія", ["🍏 Продукти", "🚕 Транспорт", "🏠 Житло", "💊 Аптека", "🎭 Розваги", "🎁 Інше"])
        if st.form_submit_button("Додати"):
            new_row = pd.DataFrame({"Дата": [datetime.now().strftime("%d.%m.%Y")], "Назва": [item], "Сума": [price], "Категорія": [cat]})
            st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
            st.session_state.df.to_csv(USER_FILE, index=False, encoding='utf-8-sig')
            st.rerun()

# Основные колонки
df = st.session_state.df
if not df.empty:
    st.metric("Всього витрачено", f"{df['Сума'].sum():,.2f} грн")
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.subheader("📋 Історія та редагування")
        st.dataframe(df, use_container_width=True, hide_index=False)
        
        # --- ФОРМА РЕДАКТИРОВАНИЯ И УДАЛЕНИЯ ---
        st.markdown("---")
        st.write("🔧 **Редагувати або видалити запис**")
        index_to_change = st.number_input("Введіть номер рядка (ліворуч у таблиці)", min_value=0, max_value=len(df)-1, step=1)
        
        with st.expander("Змінити дані вибраного рядка"):
            new_name = st.text_input("Нова назва", value=df.iloc[index_to_change]['Назва'])
            new_price = st.number_input("Нова сума", value=float(df.iloc[index_to_change]['Сума']))
            new_cat = st.selectbox("Нова категорія", ["🍏 Продукти", "🚕 Транспорт", "🏠 Житло", "💊 Аптека", "🎭 Розваги", "🎁 Інше"], 
                                    index=["🍏 Продукти", "🚕 Транспорт", "🏠 Житло", "💊 Аптека", "🎭 Розваги", "🎁 Інше"].index(df.iloc[index_to_change]['Категорія']))
            
            c1, c2 = st.columns(2)
            if c1.button("✅ Оновити запис"):
                st.session_state.df.at[index_to_change, 'Назва'] = new_name
                st.session_state.df.at[index_to_change, 'Сума'] = new_price
                st.session_state.df.at[index_to_change, 'Категорія'] = new_cat
                st.session_state.df.to_csv(USER_FILE, index=False, encoding='utf-8-sig')
                st.success("Оновлено!")
                st.rerun()
            
            if c2.button("🗑️ Видалити цей запис"):
                st.session_state.df = st.session_state.df.drop(index_to_change).reset_index(drop=True)
                st.session_state.df.to_csv(USER_FILE, index=False, encoding='utf-8-sig')
                st.warning("Видалено!")
                st.rerun()

    with col2:
        st.subheader("📊 Аналітика")
        fig = px.pie(df, values='Sumа' if 'Sumа' in df.columns else 'Сума', names='Категорія', hole=0.4)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Поки немає даних.")
