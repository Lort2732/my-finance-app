import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# --- ПРЕМИУМ ДИЗАЙН: НЕОНОВЫЙ ЗЕЛЕНЫЙ И GLASSMORPHISM ---
def apply_top_app_style():
    st.markdown(
        """
        <style>
        /* Фоновое изображение ночного города */
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?q=80&w=2000&auto=format&fit=crop");
            background-attachment: fixed;
            background-size: cover;
        }

        /* Эффект матового стекла для блоков */
        [data-testid="stVerticalBlock"] > div:has(div.stMetric), .stTabs, .stExpander {
            background: rgba(15, 15, 15, 0.75) !important;
            backdrop-filter: blur(15px);
            border-radius: 20px !important;
            border: 1px solid rgba(0, 255, 136, 0.2);
            padding: 25px !important;
            box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.8);
        }

        /* Темный сайдбар */
        [data-testid="stSidebar"] {
            background-color: rgba(0, 0, 0, 0.9) !important;
            backdrop-filter: blur(10px);
            border-right: 1px solid rgba(0, 255, 136, 0.1);
        }

        /* Текст и заголовки */
        h1, h2, h3, p, span, label, .stMarkdown {
            color: #ffffff !important;
            font-family: 'Inter', sans-serif;
        }

        /* НЕОНОВЫЕ ЗЕЛЕНЫЕ КНОПКИ */
        .stButton>button {
            background: linear-gradient(135deg, #00ff88 0%, #00a86b 100%) !important;
            color: #000000 !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: bold !important;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 0 15px rgba(0, 255, 136, 0.3);
            height: 45px;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 0 25px rgba(0, 255, 136, 0.6);
            color: #000000 !important;
        }

        /* Цвет баланса (Метрика) */
        [data-testid="stMetricValue"] {
            color: #00ff88 !important;
            text-shadow: 0 0 15px rgba(0, 255, 136, 0.5);
            font-size: 3rem !important;
        }

        /* Стилизация вкладок (Tabs) */
        .stTabs [data-baseweb="tab-list"] {
            gap: 20px;
        }
        .stTabs
