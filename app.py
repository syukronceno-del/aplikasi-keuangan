import streamlit as st
import pandas as pd
import datetime
from streamlit_option_menu import option_menu

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="KEUANGANKU",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS Modern
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #1e3d59 0%, #17b978 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
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

# Inisialisasi Session State Data
if 'transaksi' not in st.session_state:
    st.session_state.transaksi = pd.DataFrame(columns=["Tanggal", "Tipe", "Kategori", "Jumlah (Rp)", "Catatan"])

if 'target' not in st.session_state:
    st.session_state.target = []

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
    total_masuk = df[df["Tipe"] == "Pemasukan"]["Jumlah (Rp)"].sum() if not df.empty else 0
    total_keluar = df[df["Tipe"] == "Pengeluaran"]["Jumlah (Rp)"].sum() if not df.empty else 0
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
        if not df.empty and not df[df["Tipe"] == "Pengeluaran"].empty:
            kat_sum = df[df["Tipe"] == "Pengeluaran"].groupby("Kategori")["Jumlah (Rp)"].sum()
            st.bar_chart(kat_sum)
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
    
    # st.number_input: Aman dari bug angka hilang dan secara otomatis menyimpan nilai asli
    jumlah = c4.number_input("Nominal (Rp)", min_value=0, value=0, step=1000)
    
    # Menampilkan format Rp dengan titik pemisah ribuan secara langsung di bawahnya
    if jumlah > 0:
        c4.caption(f"Terbilang: **Rp {jumlah:,.0f}**".replace(",", "."))
        
    catatan = st.text_input("Catatan Keterangan")
    
    if st.button("💾 Simpan Transaksi", use_container_width=True):
        if jumlah > 0:
            new_row = pd.DataFrame([{"Tanggal": tgl, "Tipe": tipe, "Kategori": kategori, "Jumlah (Rp)": int(jumlah), "Catatan": catatan}])
            st.session_state.transaksi = pd.concat([st.session_state.transaksi, new_row], ignore_index=True)
            st.success(f"Berhasil menyimpan transaksi Rp {int(jumlah):,.0f}".replace(",", "."))
            st.rerun()
        else:
            st.error("Nominal transaksi harus lebih besar dari 0.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📜 Riwayat Lengkap Transaksi")
    st.dataframe(st.session_state.transaksi, use_container_width=True)

# ---------------------------------------------------------
# MENU 3: TARGET IMPIAN
# ---------------------------------------------------------
elif selected == "Target Impian":
    st.markdown("""
        <div class="main-header">
            <h2>🎯 Perencanaan Masa Depan</h2>
            <p>Rencanakan dan pantau perkembangan target tabungan impian Anda</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("➕ Buat Target Impian Baru")
    cx, cy, cz = st.columns(3)
    nama_target = cx.text_input("Nama Target (mis: Beli Rumah, Umroh)")
    target_dana = cy.number_input("Target Dana (Rp)", min_value=0, value=0, step=100000)
    dana_terkumpul = cz.number_input("Dana Terkumpul Saat Ini (Rp)", min_value=0, value=0, step=100000)
    
    if st.button("🎯 Simpan Target", use_container_width=True):
        if nama_target:
            st.session_state.target.append({"Nama": nama_target, "Target": int(target_dana), "Terkumpul": int(dana_terkumpul)})
            st.success("Target berhasil dibuat!")
            st.rerun()
        else:
            st.error("Nama target tidak boleh kosong.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🚀 Progres Pencapaian Impian")
    
    if not st.session_state.target:
        st.info("Belum ada target yang dibuat.")
    else:
        for t in st.session_state.target:
            progres = min(1.0, t["Terkumpul"] / t["Target"]) if t["Target"] > 0 else 0
            persen = progres * 100
            
            st.markdown(f"""
                <div class="css-card">
                    <h4>🎯 {t['Nama']}</h4>
                    <p>Terkumpul: <b>Rp {t['Terkumpul']:,.0f}</b> dari target <b>Rp {t['Target']:,.0f}</b> ({persen:.1f}%)</p>
                </div>
            """.replace(",", "."), unsafe_allow_html=True)
            st.progress(progres)

# ---------------------------------------------------------
# MENU 4: LAPORAN
# ---------------------------------------------------------
elif selected == "Laporan":
    st.markdown("""
        <div class="main-header">
            <h2>📈 Laporan & Unduh Data</h2>
            <p>Unduh berkas rekapitulasi data keuangan dalam format CSV</p>
        </div>
    """, unsafe_allow_html=True)
    
    df = st.session_state.transaksi
    if df.empty:
        st.warning("Belum ada data untuk diunduh.")
    else:
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(label="📥 Download Laporan (CSV)", data=csv, file_name="Laporan_Keuangan.csv", mime="text/csv", use_container_width=True)
