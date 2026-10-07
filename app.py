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
            "container": {"padding": "5px", "background-color": "#f8f9fa", "border-radius": "10px"},
            "icon": {"color": "#17b978", "font-size": "18px"},
            "nav-link": {"font-size": "14px", "text-align": "left", "margin": "2px"},
            "nav-link-selected": {"background-color": "#1e3d59", "color": "white", "font-weight": "bold"}
        }
    )

# ---------------------------------------------------------
# MENU 1: DASHBOARD
# ---------------------------------------------------------
if selected == "Dashboard":
    st.markdown("""
        <div class="main-header">
            <h2>✨ Dashboard Keuangan</h2>
            <p>Kelola arus kas dan pantau perkembangan finansial Anda secara realtime</p>
        </div>
    """, unsafe_allow_html=True)
    
    df = st.session_state.transaksi
    if not df.empty:
        total_masuk = df[df["Tipe"] == "Pemasukan"]["Jumlah (Rp)"].sum()
        total_keluar = df[df["Tipe"] == "Pengeluaran"]["Jumlah (Rp)"].sum()
    else:
        total_masuk = 0
        total_keluar = 0
        
    sisa_saldo = total_masuk - total_keluar
    
    m1, m2, m3 = st.columns(3)
    m1.metric("💵 Total Saldo", f"Rp {sisa_saldo:,.0f}".replace(",", "."))
    m2.metric("📈 Total Pemasukan", f"Rp {total_masuk:,.0f}".replace(",", "."))
    m3.metric("📉 Total Pengeluaran", f"Rp {total_keluar:,.0f}".replace(",", "."))
    
    st.markdown("<br>", unsafe_allow_html=True)
    col_left, col_right = st.columns([1.5, 1])
    
    with col_left:
        st.markdown('<div class="css-card">', unsafe_allow_html=True)
        st.subheader("📋 Transaksi Terakhir")
        if df.empty:
            st.info("Belum ada data transaksi yang dicatat.")
        else:
            st.dataframe(df.tail(5), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_right:
        st.markdown('<div class="css-card">', unsafe_allow_html=True)
        st.subheader("📊 Analisis Pengeluaran")
        if not df.empty:
            df_keluar = df[df["Tipe"] == "Pengeluaran"]
            if not df_keluar.empty:
                kat_sum = df_keluar.groupby("Kategori")["Jumlah (Rp)"].sum()
                st.bar_chart(kat_sum)
            else:
                st.caption("Belum ada data pengeluaran.")
        else:
            st.caption("Belum ada data pengeluaran.")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# MENU 2: TRANSAKSI
# ---------------------------------------------------------
elif selected == "Transaksi":
    st.markdown("""
        <div class="main-header">
            <h2>📝 Catatan Transaksi</h2>
            <p>Tambah pemasukan atau pengeluaran baru ke dalam catatan</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("➕ Form Input Transaksi")
    c1, c2 = st.columns(2)
    tgl = c1.date_input("Tanggal", datetime.date.today())
    tipe = c2.selectbox("Tipe Transaksi", ["Pemasukan", "Pengeluaran"])
    
    c3, c4 = st.columns(2)
    kategori = c3.selectbox("Kategori", [
        "Gaji / Profit", "Makanan & Minuman", "Transportasi", 
        "Belanja Bulanan", "Tagihan & Utilitas", "Hiburan", "Lainnya"
    ])
    
    jumlah_raw = c4.text_input(
        "Nominal (Rp)", 
        key="input_nominal_val", 
        on_change=format_nominal, 
        placeholder="Contoh: 1000000"
    )
    
    catatan = st.text_input("Catatan Keterangan")
    
    if st.button("💾 Simpan Transaksi", use_container_width=True):
        jumlah_clean = jumlah_raw.replace(".", "").replace(",", "").strip()
        jumlah = int(jumlah_clean) if jumlah_clean.isdigit() else 0
        
        if jumlah > 0:
            new_data = pd.DataFrame([{
                "Tanggal": tgl,
                "Tipe": tipe,
                "Kategori": kategori,
                "Jumlah (Rp)": jumlah,
                "Catatan": catatan
            }])
            st.session_state.transaksi =
