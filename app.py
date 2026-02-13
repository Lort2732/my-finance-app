import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# --- ПРЕМИУМ ДИЗАЙН (CSS) ---
def apply_top_app_style():
    st.markdown(
        """
        <style>
        /* Фон с глубоким размытием */
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?q=80&w=2000&auto=format&fit=crop");
            background-attachment: fixed;
            background-size: cover;
        }

        /* Контейнеры "Матовое стекло" */
        [data-testid="stVerticalBlock"] > div:has(div.stMetric), .stTabs, .stExpander {
            background: rgba(15, 15, 15, 0.7) !important;
            backdrop-filter: blur(12px);
            border-radius: 20px !important;
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 20px !important;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        }

        /* Сайдбар */
        [data-testid="stSidebar"] {
            background-color: rgba(0, 0, 0, 0.8) !important;
            backdrop-filter: blur(10px);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* Заголовки и текст */
        h1, h2, h3, p, span, label {
            color: #ffffff !important;
            font-family: 'Inter', sans-serif;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }

        /* Кнопки с градиентом */
        .stButton>button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: bold !important;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(118, 75, 162, 0.4);
        }

        /* Кастомизация метрик */
        [data-testid="stMetricValue"] {
            color: #00ffcc !important;
            font-size: 2.5rem !important;
        }

        /* Удаление стандартных рамок таблиц */
        .stDataFrame {
            border: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

st.set_page_config(page_title="Finance Pro v2.0", page_icon="📈", layout="wide")
apply_top_app_style()

# --- ЛОГИКА ПОЛЬЗОВАТЕЛЕЙ ---
USER_DB = "users_credentials.csv"
def load_users():
    return pd.read_csv(USER_DB).to_dict('records') if os.path.exists(USER_DB) else []

def save_user(login, password):
    users = load_users()
    if any(u['login'] == login for u in users): return False
    users.append({'login': login, 'password': password})
    pd.DataFrame(users).to_csv(USER_DB, index=False)
    return True

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_login = None

# --- ЭКРАН ВХОДА (КОМПАКТНЫЙ) ---
if not st.session_state.authenticated:
    # Создаем три колонки: боковые пустые, центральная для формы
    col_left, col_mid, col_right = st.columns([1, 1.2, 1])
    
    with col_mid:
        st.markdown("<h1 style='text-align: center;'>🏙️ FINANCE PRO</h1>", unsafe_allow_html=True)
        st.write("") # Отступ
        
        t1, t2 = st.tabs(["🔐 ВХІД", "📝 РЕЄСТРАЦІЯ"])
        
        with t1:
            with st.form("l_form"):
                l_login = st.text_input("Логін").strip().lower()
                l_pass = st.text_input("Пароль", type="password")
                submit_l = st.form_submit_button("УВІЙТИ")
                if submit_l:
                    if any(u['login'] == l_login and str(u['password']) == str(l_pass) for u in load_users()):
                        st.session_state.authenticated, st.session_state.user_login = True, l_login
                        st.rerun()
                    else: 
                        st.error("Помилка входу")
        
        with t2:
            with st.form("r_form"):
                r_login = st.text_input("Придумайте логін")
                r_pass = st.text_input("Придумайте пароль", type="password")
                submit_r = st.form_submit_button("СТВОРИТИ АКАУНТ")
                if submit_r:
                    if r_login and r_pass:
                        if save_user(r_login.strip().lower(), r_pass): 
                            st.success("Акаунт створено! Тепер увійдіть.")
                        else: 
                            st.error("Цей логін вже зайнятий")
                    else:
                        st.warning("Заповніть усі поля")
    st.stop()

# --- ОСНОВНОЙ ФУНКЦИОНАЛ ---
USER_FILE = f"expenses_{st.session_state.user_login}.csv"
if 'df' not in st.session_state:
    st.session_state.df = pd.read_csv(USER_FILE, encoding='utf-8-sig') if os.path.exists(USER_FILE) else pd.DataFrame(columns=["Дата", "Назва", "Сума", "Категорія"])

# Сайдбар с быстрыми действиями
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.write(f"### Вітаємо, {st.session_state.user_login.capitalize()}!")
    
    with st.expander("➕ НОВА ОПЕРАЦІЯ", expanded=True):
        with st.form("add_form", clear_on_submit=True):
            item = st.text_input("Назва")
            price = st.number_input("Сума", min_value=0.0)
            cat = st.selectbox("Категорія", ["🍏 Продукти", "🚕 Транспорт", "🏠 Житло", "💊 Аптека", "🎭 Розваги", "🎁 Інше"])
            if st.form_submit_button("ДОДАТИ"):
                new = pd.DataFrame({"Дата": [datetime.now().strftime("%d.%m.%Y")], "Назва": [item], "Сума": [price], "Категорія": [cat]})
                st.session_state.df = pd.concat([st.session_state.df, new], ignore_index=True)
                st.session_state.df.to_csv(USER_FILE, index=False, encoding='utf-8-sig')
                st.rerun()
    
    if st.button("🚪 ВИЙТИ"):
        st.session_state.authenticated = False
        st.rerun()

# Главный Dashboard
df = st.session_state.df
st.title("🚀 МІЙ ФІНАНСОВИЙ ДЕШБОРД")

if not df.empty:
    total = df['Сума'].sum()
    st.metric("БАЛАНС ВИТРАТ", f"{total:,.2f} ₴")

    col1, col2 = st.columns([1.6, 1])

    with col1:
        st.subheader("📝 Останні транзакції")
        # Отображение таблицы
        st.dataframe(df.style.format({"Сума": "{:.2f} ₴"}), use_container_width=True, hide_index=False)
        
        # Инструменты управления в один ряд
        st.markdown("---")
        st.subheader("🔧 Керування")
        idx = st.selectbox("Оберіть номер рядка для дій", df.index)
        
        c_edit, c_del = st.columns(2)
        with c_edit:
            with st.popover("📝 РЕДАГУВАТИ"):
                n_name = st.text_input("Нова назва", value=df.at[idx, 'Назва'])
                n_price = st.number_input("Нова сума", value=float(df.at[idx, 'Сума']))
                if st.button("ЗБЕРЕГТИ ЗМІНИ"):
                    st.session_state.df.at[idx, 'Назва'] = n_name
                    st.session_state.df.at[idx, 'Сума'] = n_price
                    st.session_state.df.to_csv(USER_FILE, index=False, encoding='utf-8-sig')
                    st.rerun()
        with c_del:
            if st.button("🗑️ ВИДАЛИТИ ЗАПИС"):
                st.session_state.df = st.session_state.df.drop(idx).reset_index(drop=True)
                st.session_state.df.to_csv(USER_FILE, index=False, encoding='utf-8-sig')
                st.rerun()

    with col2:
        st.subheader("📊 Аналіз категорій")
        fig = px.pie(df, values='Сума', names='Категорія', hole=0.6, 
                     color_discrete_sequence=px.colors.sequential.Viridis)
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font_color="white",
            margin=dict(t=0, b=0, l=0, r=0)
        )
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Ваш гаманець порожній. Час додати першу покупку!")

