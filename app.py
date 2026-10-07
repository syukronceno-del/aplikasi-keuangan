import streamlit as st
import pandas as pd
import datetime
from streamlit_option_menu import option_menu

# 1. Konfigurasi Halaman & Favicon Tab Browser
st.set_page_config(
    page_title="KEUANGANKU",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS Tampilan Modern
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #1e3d59 0%, #17b978 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #eef2f5;
    }
    .css-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border: 1px solid #eef2f5;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Inisialisasi Data Session State
if 'transaksi' not in st.session_state:
    st.session_state.transaksi = pd.DataFrame(columns=["Tanggal", "Tipe", "Kategori", "Jumlah (Rp)", "Catatan"])

if 'target' not in st.session_state:
    st.session_state.target = []

# Callback Function untuk Format Titik Otomatis
def format_nominal():
    val = st.session_state.get('input_nominal_val', '').replace('.', '').replace(',', '').strip()
    if val.isdigit() and int(val) > 0:
        st.session_state['input_nominal_val'] = f"{int(val):,}".replace(',', '.')
    else:
        st.session_state['input_nominal_val'] = ""

def format_target_dana():
    val = st.session_state.get('input_target_val', '').replace('.', '').replace(',', '').strip()
    if val.isdigit() and int(val) > 0:
        st.session_state['input_target_val'] = f"{int(val):,}".replace(',', '.')
    else:
        st.session_state['input_target_val'] = ""

def format_terkumpul_dana():
    val = st.session_state.get('input_terkumpul_val', '').replace('.', '').replace(',', '').strip()
    if val.isdigit() and int(val) > 0:
        st.session_state['input_terkumpul_val'] = f"{int(val):,}".replace(',', '.')
    else:
        st.session_state['input_terkumpul_val'] = ""

# 3. Sidebar Navigasi
with st.sidebar:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.image("logo.png", use_container_width=True)
    
    st.markdown("<h3 style='text-align: center; color: #1e3d59;'>KEUANGANKU</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    selected = option_menu(
        menu_title="Navigasi Utama",
        options=["Dashboard", "Transaksi", "Target Impian", "Laporan"],
        icons=["grid-fill", "receipt-cutoff", "trophy-fill", "file-earmark-bar-graph-fill"],
        menu_icon="compass",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#f8f9fa", "border-radius": "10px"},
            "icon": {"color": "#17b978", "font-size": "18px"},
            "nav-link": {"font-size": "14px", "text-align": "left", "margin": "2px", "--hover
