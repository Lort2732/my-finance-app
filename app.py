import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# Назва файлу бази даних
DB_FILE = "my_expenses.csv"

# Налаштування сторінки
st.set_page_config(page_title="Мій Бюджет", page_icon="💰", layout="wide")

# --- ФУНКЦІЇ РОБОТИ З ДАНИМИ ---

def load_data():
    """Завантаження даних із перевіркою на помилки"""
    if os.path.exists(DB_FILE):
        try:
            return pd.read_csv(DB_FILE, encoding='utf-8-sig')
        except Exception:
            return pd.DataFrame(columns=["Дата", "Назва", "Сума", "Категорія"])
    return pd.DataFrame(columns=["Дата", "Назва", "Сума", "Категорія"])

def save_data(df):
    """Збереження даних із обробкою помилки доступу"""
    try:
        df.to_csv(DB_FILE, index=False, encoding='utf-8-sig')
        return True
    except PermissionError:
        st.error("❌ Помилка: Закрийте файл 'my_expenses.csv' в Excel!")
        return False

# --- ІНІЦІАЛІЗАЦІЯ ---
if 'expenses_df' not in st.session_state:
    st.session_state.expenses_df = load_data()

# --- ШАПКА ---
st.title("💰 Особистий трекер витрат")
st.markdown("---")

# --- ЛІВА ПАНЕЛЬ ---
with st.sidebar:
    st.header("Додати операцію")
    with st.form("add_form", clear_on_submit=True):
        item = st.text_input("Що купили?")
        price = st.number_input("Скільки коштує (грн)", min_value=0.0, step=10.0)
        category = st.selectbox("Категорія", ["Їжа", "Транспорт", "Житло", "Розваги", "Зв'язок", "Інше"])
        submit = st.form_submit_button("Додати")

    if submit:
        if item and price > 0:
            new_row = pd.DataFrame({
                "Дата": [datetime.now().strftime("%d.%m.%Y")],
                "Назва": [item],
                "Сума": [price],
                "Категорія": [category]
            })
            
            temp_df = pd.concat([st.session_state.expenses_df, new_row], ignore_index=True)
            
            if save_data(temp_df):
                st.session_state.expenses_df = temp_df
                st.success("✅ Збережено!")
                st.rerun()
        else:
            st.warning("Введіть назву та суму!")

# --- ГОЛОВНИЙ ЕКРАН ---
df = st.session_state.expenses_df

if not df.empty:
    # Розрахунок загальної суми
    total_sum = df["Сума"].sum()
    st.metric(label="Всього витрачено", value=f"{total_sum:,.2f} грн")
    
    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.subheader("📋 Історія витрат")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        if st.button("🗑️ Очистити все"):
            if save_data(pd.DataFrame(columns=["Дата", "Назва", "Сума", "Категорія"])):
                if os.path.exists(DB_FILE):
                    os.remove(DB_FILE)
                st.session_state.expenses_df = pd.DataFrame(columns=["Дата", "Назва", "Сума", "Категорія"])
                st.rerun()

    with col2:
        st.subheader("📊 Аналітика")
        # Тут була помилка в назві колонки (Suмa -> Сума)
        fig = px.pie(df, values='Сума', names='Категорія', hole=0.4, 
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Ваша база даних порожня.")