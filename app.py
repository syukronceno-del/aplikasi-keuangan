import streamlit as st
import pandas as pd
import datetime

# 1. Konfigurasi Halaman & Favicon
st.set_page_config(
    page_title="KEUANGANKU",
    page_icon="logo.png",
    layout="wide"
)

# 2. Custom CSS untuk Mempercantik Tampilan (Card, Metric, & Sidebar)
st.markdown("""
    <style>
    /* Styling Kartu Ringkasan */
    div[data-testid="stMetric"] {
        background-color: #f8f9fa;
        padding: 18px 25px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #1e3d59;
    }
    
    /* Styling Tombol Primary */
    .stButton>button {
        background-color: #1e3d59;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Logo di Tengah Halaman Utama
col1, col2, col3 = st.columns([1, 1.5, 1])
with col2:
    st.image("logo.png", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Inisialisasi Data Transaksi & Target
if 'transaksi' not in st.session_state:
    st.session_state.transaksi = pd.DataFrame(columns=["Tanggal", "Tipe", "Kategori", "Jumlah (Rp)", "Catatan"])

if 'target' not in st.session_state:
    st.session_state.target = []

# 4. Sidebar Navigasi yang Lebih Menarik (Ber-Ikon)
st.sidebar.image("logo.png", width=120)
st.sidebar.title("📌 Menu Utama")

menu = st.sidebar.radio(
    "Pilih Halaman:",
    ["📊 Dashboard Utama", "📝 Catatan Transaksi", "🎯 Target Masa Depan", "📈 Laporan & Unduh"]
)

# ---------------------------------------------------------
# MENU 1: DASHBOARD
# ---------------------------------------------------------
if menu == "📊 Dashboard Utama":
    st.title("📊 Dashboard Keuangan")
    st.caption("Pantau seluruh kondisi finansial Anda secara real-time.")
    
    df = st.session_state.transaksi
    total_masuk = df[df['Tipe'] == 'Pemasukan']['Jumlah (Rp)'].sum() if not df.empty else 0
    total_keluar = df[df['Tipe'] == 'Pengeluaran']['Jumlah (Rp)'].sum() if not df.empty else 0
    sisa_saldo = total_masuk - total_keluar
    
    # Ringkasan Saldo Berbentuk Kartu
    m1, m2, m3 = st.columns(3)
    m1.metric("💰 Total Saldo", f"Rp {sisa_saldo:,.0f}")
    m2.metric("📈 Total Pemasukan", f"Rp {total_masuk:,.0f}")
    m3.metric("📉 Total Pengeluaran", f"Rp {total_keluar:,.0f}")
    
    st.markdown("---")
    
    # Visualisasi Data (Grafik)
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("📑 5 Transaksi Terakhir")
        if df.empty:
            st.info("Belum ada data transaksi.")
        else:
            st.dataframe(df.tail(5), use_container_width=True)
            
    with c2:
        st.subheader("📊 Komposisi Pengeluaran")
        df_keluar = df[df['Tipe'] == 'Pengeluaran']
        if not df_keluar.empty:
            kat_sum = df_keluar.groupby('Kategori')['Jumlah (Rp)'].sum()
            st.bar_chart(kat_sum)
        else:
            st.caption("Belum ada pengeluaran dicatat.")

# ---------------------------------------------------------
# MENU 2: CATATAN TRANSAKSI
# ---------------------------------------------------------
elif menu == "📝 Catatan Transaksi":
    st.title("📝 Tambah Transaksi Baru")
    
    with st.form("form_transaksi", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        tgl = col_a.date_input("Tanggal Transaksi", datetime.date.today())
        tipe = col_b.selectbox("Jenis Transaksi", ["Pemasukan", "Pengeluaran"])
        
        col_c, col_d = st.columns(2)
        kategori = col_c.selectbox("Kategori", [
            "Gaji & Profit", "Makanan & Minuman", "Transportasi", 
            "Belanja Bulanan", "Tagihan & Utilitas", "Hiburan", "Lainnya"
        ])
        jumlah = col_d.number_input("Nominal (Rp)", min_value=0, step=10000)
        
        catatan = st.text_input("Keterangan Tambahan")
        
        submit = st.form_submit_button("💾 Simpan Transaksi")
        
        if submit and jumlah > 0:
            new_data = pd.DataFrame([{
                "Tanggal": tgl,
                "Tipe": tipe,
                "Kategori": kategori,
                "Jumlah (Rp)": jumlah,
                "Catatan": catatan
            }])
            st.session_state.transaksi = pd.concat([st.session_state.transaksi, new_data], ignore_index=True)
            st.success("Berhasil menyimpan transaksi!")

    st.markdown("---")
    st.subheader("📜 Riwayat Semua Transaksi")
    st.dataframe(st.session_state.transaksi, use_container_width=True)

# ---------------------------------------------------------
# MENU 3: TARGET MASA DEPAN
# ---------------------------------------------------------
elif menu == "🎯 Target Masa Depan":
    st.title("🎯 Perencanaan Masa Depan (Financial Goals)")
    
    st.subheader("➕ Buat Impian / Target Baru")
    with st.form("form_target", clear_on_submit=True):
        col_x, col_y, col_z = st.columns(3)
        nama_target = col_x.text_input("Nama Target (mis: Beli Rumah, Umroh)")
        target_dana = col_y.number_input("Target Dana (Rp)", min_value=0, step=500000)
        dana_terkumpul = col_z.number_input("Dana Terkumpul (Rp)", min_value=0, step=100000)
        
        submit_target = st.form_submit_button("🎯 Tambahkan Target")
        if submit_target and nama_target:
            st.session_state.target.append({
                "Nama": nama_target,
                "Target": target_dana,
                "Terkumpul": dana_terkumpul
            })
            st.success("Target impian berhasil dibuat!")

    st.markdown("---")
    st.subheader("🚀 Progres Pencapaian Impian Anda")
    
    if not st.session_state.target:
        st.info("Belum ada target yang dibuat.")
    else:
        for t in st.session_state.target:
            progres = min(1.0, t["Terkumpul"] / t["Target"]) if t["Target"] > 0 else 0
            persen = progres * 100
            
            with st.container():
                st.write(f"### {t['Nama']}")
                st.write(f"Terkumpul: **Rp {t['Terkumpul']:,.0f}** dari target **Rp {t['Target']:,.0f}** ({persen:.1f}%)")
                st.progress(progres)
                st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# MENU 4: LAPORAN
# ---------------------------------------------------------
elif menu == "📈 Laporan & Unduh":
    st.title("📈 Laporan Keuangan Lengkap")
    df = st.session_state.transaksi
    
    if df.empty:
        st.warning("Belum ada data untuk diunduh.")
    else:
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Laporan Format CSV",
            data=csv,
            file_name="Laporan_Keuangan.csv",
            mime="text/csv"
        )
