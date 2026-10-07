import streamlit as st
import pandas as pd
import datetime

# 1. Konfigurasi Halaman & Favicon Tab Browser
st.set_page_config(
    page_title="KEUANGANKU",
    page_icon="logo.png",
    layout="wide"
)

# 2. Menampilkan Logo di Tengah Halaman Utama
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo.png", use_container_width=True)

st.markdown("---")

# Initialize Session State untuk simpan data transaksi sementara
if 'transaksi' not in st.session_state:
    st.session_state.transaksi = pd.DataFrame(columns=["Tanggal", "Tipe", "Kategori", "Jumlah (Rp)", "Catatan"])

if 'target' not in st.session_state:
    st.session_state.target = []

# 3. Sidebar Menu
st.sidebar.title("📌 Navigation")
menu = st.sidebar.radio("Pilih Menu:", [
    "Dashboard", 
    "Catatan Transaksi", 
    "Perencanaan Masa Depan", 
    "Laporan"
])

# ---------------------------------------------------------
# MENU 1: DASHBOARD
# ---------------------------------------------------------
if menu == "Dashboard":
    st.header("📊 Dashboard Keuangan")
    
    df = st.session_state.transaksi
    total_masuk = df[df['Tipe'] == 'Pemasukan']['Jumlah (Rp)'].sum() if not df.empty else 0
    total_keluar = df[df['Tipe'] == 'Pengeluaran']['Jumlah (Rp)'].sum() if not df.empty else 0
    sisa_saldo = total_masuk - total_keluar
    
    # Ringkasan Saldo
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Saldo", f"Rp {sisa_saldo:,.0f}")
    m2.metric("Pemasukan", f"Rp {total_masuk:,.0f}")
    m3.metric("Pengeluaran", f"Rp {total_keluar:,.0f}")
    
    st.markdown("---")
    st.subheader("💡 Ringkasan Aktivitas")
    if df.empty:
        st.info("Belum ada data transaksi. Tambahkan transaksi baru di menu **Catatan Transaksi**.")
    else:
        st.dataframe(df.tail(5), use_container_width=True)

# ---------------------------------------------------------
# MENU 2: CATATAN TRANSAKSI
# ---------------------------------------------------------
elif menu == "Catatan Transaksi":
    st.header("📝 Catat Transaksi Baru")
    
    with st.form("form_transaksi", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        tgl = col_a.date_input("Tanggal", datetime.date.today())
        tipe = col_b.selectbox("Tipe Transaksi", ["Pemasukan", "Pengeluaran"])
        
        kategori = st.selectbox("Kategori", [
            "Gaji / Usaha", "Makanan & Minuman", "Transportasi", 
            "Belanja & Tagihan", "Hiburan", "Lainnya"
        ])
        
        jumlah = st.number_input("Jumlah (Rp)", min_value=0, step=5000)
        catatan = st.text_input("Catatan / Keterangan")
        
        submit = st.form_submit_button("Simpan Transaksi")
        
        if submit:
            new_data = pd.DataFrame([{
                "Tanggal": tgl,
                "Tipe": tipe,
                "Kategori": kategori,
                "Jumlah (Rp)": jumlah,
                "Catatan": catatan
            }])
            st.session_state.transaksi = pd.concat([st.session_state.transaksi, new_data], ignore_index=True)
            st.success("Transaksi berhasil disimpan!")

    st.markdown("---")
    st.subheader("📜 Riwayat Transaksi")
    st.dataframe(st.session_state.transaksi, use_container_width=True)

# ---------------------------------------------------------
# MENU 3: PERENCANAAN MASA DEPAN
# ---------------------------------------------------------
elif menu == "Perencanaan Masa Depan":
    st.header("🎯 Perencanaan Masa Depan (Financial Goals)")
    
    st.subheader("Tambah Target Tabungan / Impian")
    with st.form("form_target", clear_on_submit=True):
        nama_target = st.text_input("Nama Impian (misal: Dana Darurat, Beli Rumah, Umroh)")
        target_dana = st.number_input("Target Dana (Rp)", min_value=0, step=100000)
        dana_terkumpul = st.number_input("Dana Terkumpul Saat Ini (Rp)", min_value=0, step=100000)
        
        submit_target = st.form_submit_button("Tambah Target")
        if submit_target and nama_target:
            st.session_state.target.append({
                "Nama": nama_target,
                "Target": target_dana,
                "Terkumpul": dana_terkumpul
            })
            st.success("Target impian berhasil ditambahkan!")
            
    st.markdown("---")
    st.subheader("🚀 Progres Target Kamu")
    if not st.session_state.target:
        st.info("Belum ada target masa depan yang dibuat.")
    else:
        for t in st.session_state.target:
            progres = min(1.0, t["Terkumpul"] / t["Target"]) if t["Target"] > 0 else 0
            st.write(f"**{t['Nama']}** — Rp {t['Terkumpul']:,.0f} / Rp {t['Target']:,.0f}")
            st.progress(progres)

# ---------------------------------------------------------
# MENU 4: LAPORAN
# ---------------------------------------------------------
elif menu == "Laporan":
    st.header("📈 Laporan & Unduh Data")
    df = st.session_state.transaksi
    
    if df.empty:
        st.warning("Belum ada data transaksi untuk diunduh.")
    else:
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Data Laporan (CSV)",
            data=csv,
            file_name="Laporan_Keuanganku.csv",
            mime="text/csv"
        )
