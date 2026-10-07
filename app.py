import streamlit as st
import pandas as pd
import os
from datetime import datetime
import io

# --- KONFIGURASI HALAMAN ---
st.set_page_config(layout="wide", page_title="Aplikasi Keuangan Bang Syukron")

# --- KONFIGURASI AKUN LOGIN ---
USER_CREDENTIALS = {
    "admin": "12345"
}

# --- INISIALISASI SESSION STATE ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# --- FUNGSI CUSTOM CARD HTML/CSS ---
def custom_card(title, value, date_text, gradient_color, text_color="white"):
    card_html = f"""
    <div style="
        border-radius: 12px;
        background-image: {gradient_color};
        padding: 20px;
        color: {text_color};
        margin-bottom: 20px;
        font-family: 'Open Sans', sans-serif;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 160px;
    ">
        <div style="font-size: 16px; font-weight: 500; opacity: 0.9;">{title}</div>
        <div style="font-size: 28px; font-weight: 700; padding: 15px 0;">{value}</div>
        <div style="font-size: 12px; font-weight: 400; opacity: 0.8; margin-top: auto;">{date_text}</div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

# --- HALAMAN LOGIN ---
def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("")
        st.write("")
        st.title("🔒 Login Aplikasi Keuangan")
        with st.form("form_login"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Login")

            if submit_button:
                if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                    st.session_state["logged_in"] = True
                    st.success("Login berhasil!")
                    st.rerun()
                else:
                    st.error("Username atau password salah!")

# --- HALAMAN UTAMA APLIKASI ---
def main_app():
    DATA_FILE = "keuangan.csv"

    if not os.path.exists(DATA_FILE):
        df_init = pd.DataFrame(columns=["Tanggal", "Kategori", "Jenis", "Jumlah", "Keterangan"])
        df_init.to_csv(DATA_FILE, index=False)

    df = pd.read_csv(DATA_FILE)

    # --- SIDEBAR MENU ---
    with st.sidebar:
        st.title("💰 KEUANGAN KU")
        st.divider()
        st.subheader("👨‍💼 Administrator")
        st.write("Bang Syukron")
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state["logged_in"] = False
            st.rerun()

    # --- JUDUL UTAMA ---
    st.header("📌 Dashboard")
    st.write("Selamat Datang, Bang Syukron! 👋")
    
    if not df.empty:
        df["Tanggal"] = pd.to_datetime(df["Tanggal"])
        df["Bulan_Tahun"] = df["Tanggal"].dt.strftime("%Y-%m")
        hari_ini = datetime.today().strftime("%Y-%m-%d")
        bulan_ini_str = datetime.today().strftime("%Y-%m")
        tahun_ini_str = datetime.today().strftime("%Y")

        # --- HITUNG SIKLUS PEMASUKAN ---
        p_hari_ini = df[(df["Jenis"] == "Pemasukan") & (df["Tanggal"].dt.strftime("%Y-%m-%d") == hari_ini)]["Jumlah"].sum()
        p_bulan_ini = df[(df["Jenis"] == "Pemasukan") & (df["Bulan_Tahun"] == bulan_ini_str)]["Jumlah"].sum()
        p_tahun_ini = df[(df["Jenis"] == "Pemasukan") & (df["Tanggal"].dt.strftime("%Y") == tahun_ini_str)]["Jumlah"].sum()
        p_total = df[df["Jenis"] == "Pemasukan"]["Jumlah"].sum()

        # --- HITUNG SIKLUS PENGELUARAN ---
        k_hari_ini = df[(df["Jenis"] == "Pengeluaran") & (df["Tanggal"].dt.strftime("%Y-%m-%d") == hari_ini)]["Jumlah"].sum()
        k_bulan_ini = df[(df["Jenis"] == "Pengeluaran") & (df["Bulan_Tahun"] == bulan_ini_str)]["Jumlah"].sum()
        k_tahun_ini = df[(df["Jenis"] == "Pengeluaran") & (df["Tanggal"].dt.strftime("%Y") == tahun_ini_str)]["Jumlah"].sum()
        k_total = df[df["Jenis"] == "Pengeluaran"]["Jumlah"].sum()

        saldo_total = p_total - k_total

        # --- TAMPILAN DASHBOARD KARTU ---
        st.write("#### Ringkasan Transaksi")
        
        row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)
        
        with row1_col1:
            custom_card("Pemasukan Hari Ini", f"Rp {p_hari_ini:,.0f}", datetime.today().strftime("%d-%m-%Y"), "linear-gradient(135deg, #1d90ff, #00bfff)")
        with row1_col2:
            custom_card("Pemasukan Bulan Ini", f"Rp {p_bulan_ini:,.0f}", datetime.today().strftime("%B %Y"), "linear-gradient(135deg, #ff6b6b, #ff8787)")
        with row1_col3:
            custom_card("Pemasukan Tahun Ini", f"Rp {p_tahun_ini:,.0f}", datetime.today().strftime("%Y"), "linear-gradient(135deg, #f0932b, #ffbe76)")
        with row1_col4:
            custom_card("Seluruh Pemasukan", f"Rp {p_total:,.0f}", "Semua Periode", "linear-gradient(135deg, #30336b, #130f40)")

        row2_col1, row2_col2, row2_col3, row2_col4 = st.columns(4)
        
        with row2_col1:
            custom_card("Pengeluaran Hari Ini", f"Rp {k_hari_ini:,.0f}", datetime.today().strftime("%d-%m-%Y"), "linear-gradient(135deg, #8c7ae6, #9c88ff)")
        with row2_col2:
            custom_card("Pengeluaran Bulan Ini", f"Rp {k_bulan_ini:,.0f}", datetime.today().strftime("%B %Y"), "linear-gradient(135deg, #e056fd, #be2edd)")
        with row2_col3:
            custom_card("Pengeluaran Tahun Ini", f"Rp {k_tahun_ini:,.0f}", datetime.today().strftime("%Y"), "linear-gradient(135deg, #4834d4, #686de0)")
        with row2_col4:
            custom_card("Sisa Saldo Anda (Total)", f"Rp {saldo_total:,.0f}", "Semua Periode", "linear-gradient(135deg, #c0392b, #e74c3c)")

        st.divider()

        # --- FORM INPUT TRANSAKSI BARU ---
        st.subheader("➕ Tambah Transaksi Baru")
        with st.form("form_transaksi", clear_on_submit=True):
            col_in1, col_in2, col_in3 = st.columns([2, 2, 3])
            with col_in1:
                tanggal = st.date_input("Tanggal", datetime.today())
                jenis = st.selectbox("Jenis", ["Pemasukan", "Pengeluaran"])
            with col_in2:
                jumlah = st.number_input("Jumlah (Rp)", min_value=0, step=1000)
                kategori = st.text_input("Kategori", placeholder="Misal: Makanan, Gaji, Tagihan")
            with col_in3:
                keterangan = st.text_area("Keterangan", placeholder="Detail transaksi")
            
            submitted = st.form_submit_button("Simpan Transaksi", use_container_width=True)

            if submitted:
                new_data = pd.DataFrame({
                    "Tanggal": [tanggal.strftime("%Y-%m-%d")],
                    "Kategori": [kategori.title()],
                    "Jenis": [jenis],
                    "Jumlah": [jumlah],
                    "Keterangan": [keterangan]
                })
                df_updated = pd.concat([df, new_data], ignore_index=True)
                df_updated.to_csv(DATA_FILE, index=False)
                st.success("Transaksi berhasil disimpan!")
                st.rerun()

        # --- LAPORAN DETAIL TRANSAKSI ---
        st.divider()
        st.subheader("📋 Detail Transaksi")

        list_bulan = df["Bulan_Tahun"].unique().tolist()
        list_bulan.sort(reverse=True)
        
        if 'bulan_pilihan_detail' not in st.session_state:
            st.session_state['bulan_pilihan_detail'] = list_bulan[0]

        bulan_terpilih = st.selectbox("Filter Detail Transaksi per Bulan:", list_bulan, key='bulan_pilihan_detail')

        df_filtered = df[df["Bulan_Tahun"] == bulan_terpilih].copy()
        df_display = df_filtered[["Tanggal", "Kategori", "Jenis", "Jumlah", "Keterangan"]].copy()
        df_display["Tanggal"] = df_display["Tanggal"].dt.strftime("%Y-%m-%d")
        st.dataframe(df_display, use_container_width=True)

        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_display.to_excel(writer, index=False, sheet_name='Laporan Keuangan')
        
        st.download_button(
            label="📥 Unduh Laporan (Excel)",
            data=buffer.getvalue(),
            file_name=f"Laporan_Keuangan_{bulan_terpilih}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

        # --- GRAFIK PENGELUARAN & PEMASUKAN ---
        st.divider()
        st.subheader(f"📊 Grafik Keuangan Bulan Ini ({datetime.today().strftime('%B %Y')})")
        col_grf1, col_grf2 = st.columns(2)
        
        df_bulan_ini = df[df["Bulan_Tahun"] == bulan_ini_str]
        
        with col_grf1:
            st.write("#### 💸 Pengeluaran per Kategori")
            df_peng_bulan = df_bulan_ini[df_bulan_ini["Jenis"] == "Pengeluaran"]
            if not df_peng_bulan.empty:
                kat_sum = df_peng_bulan.groupby("Kategori")["Jumlah"].sum().reset_index()
                st.bar_chart(data=kat_sum, x="Kategori", y="Jumlah", color="#be2edd")
            else:
                st.info("Belum ada data pengeluaran bulan ini.")

        with col_grf2:
            st.write("#### 💵 Pemasukan per Kategori")
            df_pem_bulan = df_bulan_ini[df_bulan_ini["Jenis"] == "Pemasukan"]
            if not df_pem_bulan.empty:
                pem_kat_sum = df_pem_bulan.groupby("Kategori")["Jumlah"].sum().reset_index()
                st.bar_chart(data=pem_kat_sum, x="Kategori", y="Jumlah", color="#ff6b6b")
            else:
                st.info("Belum ada data pemasukan bulan ini.")

    else:
        st.info("Belum ada data transaksi. Silakan input transaksi pertama!")
        with st.form("form_transaksi_awal", clear_on_submit=True):
            tanggal = st.date_input("Tanggal", datetime.today())
            jenis = st.selectbox("Jenis", ["Pemasukan", "Pengeluaran"])
            kategori = st.text_input("Kategori")
            jumlah = st.number_input("Jumlah (Rp)", min_value=0, step=1000)
            keterangan = st.text_input("Keterangan")
            submitted = st.form_submit_button("Simpan Transaksi Pertama")

            if submitted:
                new_data = pd.DataFrame({
                    "Tanggal": [tanggal.strftime("%Y-%m-%d")],
                    "Kategori": [kategori.title()],
                    "Jenis": [jenis],
                    "Jumlah": [jumlah],
                    "Keterangan": [keterangan]
                })
                new_data.to_csv(DATA_FILE, index=False)
                st.success("Transaksi pertama berhasil disimpan!")
                st.rerun()

# --- NAVIGASI HALAMAN ---
if st.session_state["logged_in"]:
    main_app()
else:
    login_page()