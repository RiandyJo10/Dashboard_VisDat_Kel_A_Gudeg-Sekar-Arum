
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path
from html import escape


st.set_page_config(
    page_title="Dashboard Gudeg Sekar Arum 2025",
    layout="wide",
    initial_sidebar_state="collapsed"
)

COKELAT = "#C47A42"
HIJAU = "#477B70"
BIRU = "#4C93BD"
GELAP = "#3D241C"
PUTIH = "#FFFCF8"
ABU = "#C9CED3"

WARNA_OUTLET = {
    "Malioboro": COKELAT,
    "Wijilan": HIJAU,
    "Kaliurang": "#7D8FB3",
    "Godean": "#B59A7B"
}

BULAN = [
    "Jan", "Feb", "Mar", "Apr", "Mei", "Jun",
    "Jul", "Agu", "Sep", "Okt", "Nov", "Des"
]

st.markdown("""
<style>
.stApp {
    background-color: #FCF7EF;
    color: #3D241C;
}
.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
h1, h2, h3 {
    color: #3D241C !important;
}
.header {
    background: linear-gradient(110deg, #5B392B, #A9673F);
    padding: 26px 30px;
    border-radius: 18px;
    margin-bottom: 22px;
}
.header h1 {
    color: white !important;
    margin: 0;
    font-size: 2rem;
}
.header p {
    color: #F7E7D6;
    margin: 10px 0 0;
}
.kpi {
    background: #FFFCF8;
    border: 1px solid #EADFD2;
    border-radius: 14px;
    padding: 18px 15px;
    min-height: 135px;
}
.kpi-label {
    color: #78685D;
    font-size: 0.85rem;
    font-weight: 600;
}
.kpi-value {
    color: #3D241C;
    font-size: clamp(1.1rem, 1.65vw, 1.65rem);
    font-weight: 800;
    margin-top: 12px;
    overflow-wrap: anywhere;
}
.kpi-note {
    color: #8A7B70;
    font-size: 0.75rem;
    margin-top: 7px;
}
.insight {
    background: #FFF6E9;
    border-left: 4px solid #C47A42;
    border-radius: 6px;
    padding: 12px 16px;
    margin: 6px 0 16px;
    color: #3D241C;
    font-size: 0.94rem;
    line-height: 1.6;
}
div[data-testid="stPlotlyChart"] {
    background: #FFFCF8;
    border: 1px solid #EADFD2;
    border-radius: 14px;
    padding: 8px;
}
.filter-label {
    color: #36313B;
    font-size: 0.875rem;
    margin-bottom: 0.35rem;
}
/* Dropdown tanpa input ketik: tombol st.popover menggantikan selectbox. */
/* HANYA tombol utama dua filter, bukan tombol pilihan pada menu. */
.st-key-filter_outlet div[data-testid="stPopover"] > button,
.st-key-filter_kanal div[data-testid="stPopover"] > button,
.st-key-filter_outlet div[data-testid="stPopover"] > div > button,
.st-key-filter_kanal div[data-testid="stPopover"] > div > button {
    width: 100% !important;
    min-height: 42px !important;
    justify-content: space-between !important;
    background: linear-gradient(110deg, #5B392B, #A9673F) !important;
    background-color: #5B392B !important;
    color: #FFFFFF !important;
    border: 1px solid #A9673F !important;
    border-radius: 10px !important;
    box-shadow: none !important;
    text-align: left !important;
}
/* Penjagaan tambahan apabila wrapper popover berbeda antarrilis. */
.st-key-filter_outlet [data-testid="stPopover"] button[kind="secondary"],
.st-key-filter_kanal [data-testid="stPopover"] button[kind="secondary"] {
    background: linear-gradient(110deg, #5B392B, #A9673F) !important;
    color: #FFFFFF !important;
    border-color: #A9673F !important;
}
.st-key-filter_outlet [data-testid="stPopover"] > button *,
.st-key-filter_kanal [data-testid="stPopover"] > button * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    stroke: #FFFFFF !important;
}
.st-key-filter_outlet [data-testid="stPopover"] > button:hover,
.st-key-filter_kanal [data-testid="stPopover"] > button:hover {
    background: linear-gradient(110deg, #684331, #B27B51) !important;
}
/* Hanya ikon panah bawaan Streamlit; geser ke ujung kanan. */
.st-key-filter_outlet [data-testid="stPopover"] > button,
.st-key-filter_kanal [data-testid="stPopover"] > button {
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    gap: 10px !important;
}
.st-key-filter_outlet [data-testid="stPopover"] > button svg,
.st-key-filter_kanal [data-testid="stPopover"] > button svg {
    margin-left: auto !important;
    flex-shrink: 0 !important;
}
.st-key-filter_outlet [data-testid="stPopover"] > button [data-testid="stMarkdownContainer"],
.st-key-filter_kanal [data-testid="stPopover"] > button [data-testid="stMarkdownContainer"] {
    flex: 1 1 auto !important;
    text-align: left !important;
}
/* Rentang tanggal: pertahankan penampilan yang sudah berhasil. */
.st-key-filter_tanggal [data-baseweb="input"],
.st-key-filter_tanggal [data-baseweb="base-input"],
.st-key-filter_tanggal [data-baseweb="input"] > div,
.st-key-filter_tanggal [data-baseweb="base-input"] > div,
.st-key-filter_tanggal [data-testid="stDateInputField"],
.st-key-filter_tanggal input {
    background: linear-gradient(110deg, #5B392B, #A9673F) !important;
    color: #FFFFFF !important;
    border-color: #A9673F !important;
}
.st-key-filter_tanggal [data-baseweb="input"] > div > div,
.st-key-filter_tanggal [data-baseweb="base-input"] > div > div {
    background-color: transparent !important;
}
.st-key-filter_tanggal [data-baseweb="input"],
.st-key-filter_tanggal [data-baseweb="base-input"] {
    border-radius: 10px !important;
    min-height: 42px;
}
.st-key-filter_tanggal input,
.st-key-filter_tanggal [data-testid="stDateInputField"] * {
    color: white !important;
    -webkit-text-fill-color: white !important;
}
.st-key-filter_tanggal svg {
    color: white !important;
    stroke: white !important;
}
/* Petunjuk penggunaan: jaga kontras saat dibuka */
div[data-testid="stExpander"] details,
div[data-testid="stExpander"] details summary,
div[data-testid="stExpander"] details > div {
    background-color: #FFFCF8 !important;
    color: #3D241C !important;
}
div[data-testid="stExpander"] details * {
    color: #3D241C !important;
    -webkit-text-fill-color: #3D241C !important;
}

/* Layout 2x2 rapi: ruang antar-komponen dijaga agar tidak bertabrakan. */
.block-container {
    max-width: 1450px;
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
}
.header {
    padding: 20px 24px !important;
    margin-bottom: 18px !important;
    border-radius: 14px !important;
}
.header h1 {font-size: 1.65rem !important; line-height: 1.35 !important;}
.header p {font-size: .89rem !important; margin-top: 8px !important;}
.kpi {min-height: 110px !important; padding: 14px !important;}
.kpi-label {font-size: .78rem !important; line-height: 1.35 !important;}
.kpi-value {font-size: 1.3rem !important; margin-top: 9px !important;}
.kpi-note {font-size: .73rem !important; margin-top: 6px !important;}
.insight {
    padding: 10px 12px !important;
    margin: 8px 0 12px !important;
    font-size: .84rem !important;
    line-height: 1.55 !important;
    overflow-wrap: anywhere;
}
.filter-label {font-size: .86rem !important; margin-bottom: .35rem !important;}
.st-key-filter_outlet [data-testid="stPopover"] > button,
.st-key-filter_kanal [data-testid="stPopover"] > button {min-height: 42px !important;}
.st-key-filter_tanggal [data-baseweb="input"] {min-height: 42px !important;}
div[data-testid="stPlotlyChart"] {
    padding: 10px 8px !important;
    border-radius: 12px !important;
    overflow: hidden;
}
/* Jangan menekan gap semua blok sampai judul, insight, dan grafik bertumpuk. */
[data-testid="stVerticalBlock"] {gap: .85rem !important;}
[data-testid="stHorizontalBlock"] {gap: 1.1rem !important;}
.stApp h3 {font-size: 1.04rem !important; line-height: 1.35 !important; margin-bottom: .25rem !important;}
[data-testid="stCaptionContainer"] {line-height: 1.45 !important;}

</style>
""", unsafe_allow_html=True)


def angka(nilai):
    return f"{nilai:,.0f}".replace(",", ".")


def rupiah(nilai):
    return f"Rp {angka(nilai)}"


def ringkas(nilai):
    if abs(nilai) >= 1_000_000_000:
        hasil = f"{nilai / 1_000_000_000:.2f}"
        return "Rp " + hasil.replace(".", ",") + " M"
    if abs(nilai) >= 1_000_000:
        hasil = f"{nilai / 1_000_000:.2f}"
        return "Rp " + hasil.replace(".", ",") + " Jt"
    return rupiah(nilai)


def persen(nilai):
    return f"{nilai:.2f}".replace(".", ",") + "%"


def skor(nilai):
    return f"{nilai:.2f}".replace(".", ",")


def bersihkan_angka(series, minus_nol=False):
    teks = (
        series.astype("string")
        .str.strip()
        .str.replace(",", "", regex=False)
        .str.replace(r"(?i)rp\.?", "", regex=True)
        .str.replace(r"\s+", "", regex=True)
    )
    if minus_nol:
        teks = teks.replace({"-": "0"})
    return pd.to_numeric(teks, errors="coerce")


def kartu(label, nilai, catatan):
    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-label">{escape(label)}</div>
            <div class="kpi-value">{escape(nilai)}</div>
            <div class="kpi-note">{escape(catatan)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def insight(teks):
    st.markdown(
        f'<div class="insight">{escape(teks)}</div>',
        unsafe_allow_html=True
    )


def gaya(fig, tinggi=440):
    fig.update_layout(
        template="plotly_white",
        height=min(tinggi, 330),
        paper_bgcolor=PUTIH,
        plot_bgcolor=PUTIH,
        font=dict(family="Arial", size=11, color=GELAP),
        margin=dict(l=70, r=48, t=40, b=65),
        hoverlabel=dict(bgcolor="white", font_size=11)
    )
    return fig


def tampil(fig, key):
    st.plotly_chart(
        fig,
        use_container_width=True,
        key=key,
        config={"displaylogo": False}
    )



lokasi_file = (
    Path(__file__).parent
    / "Data_Simulasi_Penjualan_Gudeg_Jogja_2025.csv"
)

if not lokasi_file.exists():
    st.error("File CSV tidak ditemukan.")
    st.stop()

df = pd.read_csv(lokasi_file, encoding="utf-8-sig")
df.columns = df.columns.str.strip()

for kolom in [
    "Omzet_Bersih_Rp",
    "Omzet_Gudeg_Rp",
    "Omzet_Oleh_Oleh_Rp"
]:
    df[kolom] = bersihkan_angka(
        df[kolom],
        minus_nol=True
    )

for kolom in [
    "Jumlah_Transaksi",
    "Jumlah_Ulasan",
    "Rating_Rata_rata"
]:
    df[kolom] = pd.to_numeric(
        df[kolom],
        errors="coerce"
    )

df["Tanggal"] = pd.to_datetime(
    df["Tanggal"],
    format="%d/%m/%Y",
    errors="coerce"
)

wajib = [
    "Omzet_Bersih_Rp",
    "Omzet_Gudeg_Rp",
    "Omzet_Oleh_Oleh_Rp",
    "Jumlah_Transaksi",
    "Tanggal",
    "Outlet",
    "Kanal_Penjualan"
]

gagal = [k for k in wajib if df[k].isna().any()]

if gagal:
    st.error("Kolom yang masih memiliki data tidak valid:")
    st.write(gagal)
    st.stop()


st.markdown("""
<div class="header">
    <h1>Gudeg Sekar Arum</h1>
    <p>Dashboard Kinerja Penjualan 2025 |
       Visualisasi Analisis Interaktif</p>
</div>
""", unsafe_allow_html=True)

st.subheader("Filter Data Penjualan")

f1, f2, f3 = st.columns(3)

# Popover + tombol pilihan: benar-benar tanpa kolom ketik/search.
# Tidak mengubah logika filter yang digunakan oleh KPI dan grafik.
opsi_outlet = ["Semua Outlet"] + sorted(df["Outlet"].unique().tolist())
opsi_kanal = ["Semua Kanal"] + sorted(df["Kanal_Penjualan"].unique().tolist())
if st.session_state.get("pilihan_outlet_menu") not in opsi_outlet:
    st.session_state["pilihan_outlet_menu"] = "Semua Outlet"
if st.session_state.get("pilihan_kanal_menu") not in opsi_kanal:
    st.session_state["pilihan_kanal_menu"] = "Semua Kanal"

with f1:
    st.markdown('<div class="filter-label">Outlet</div>', unsafe_allow_html=True)
    with st.container(key="filter_outlet"):
        with st.popover(st.session_state["pilihan_outlet_menu"], use_container_width=True):
            for i, nama in enumerate(opsi_outlet):
                if st.button(nama, key=f"pilih_outlet_{i}", use_container_width=True):
                    st.session_state["pilihan_outlet_menu"] = nama
                    st.rerun()
    pilihan_outlet = st.session_state["pilihan_outlet_menu"]

with f2:
    st.markdown('<div class="filter-label">Kanal Penjualan</div>', unsafe_allow_html=True)
    with st.container(key="filter_kanal"):
        with st.popover(st.session_state["pilihan_kanal_menu"], use_container_width=True):
            for i, nama in enumerate(opsi_kanal):
                if st.button(nama, key=f"pilih_kanal_{i}", use_container_width=True):
                    st.session_state["pilihan_kanal_menu"] = nama
                    st.rerun()
    pilihan_kanal = st.session_state["pilihan_kanal_menu"]

with f3:
    pilihan_tanggal = st.date_input(
        "Rentang Tanggal",
        value=(
            df["Tanggal"].min().date(),
            df["Tanggal"].max().date()
        ),
        min_value=df["Tanggal"].min().date(),
        max_value=df["Tanggal"].max().date(),
        format="DD/MM/YYYY",
        key="filter_tanggal"
    )

data = df.copy()

if pilihan_outlet != "Semua Outlet":
    data = data[data["Outlet"] == pilihan_outlet]

if pilihan_kanal != "Semua Kanal":
    data = data[
        data["Kanal_Penjualan"] == pilihan_kanal
    ]

if len(pilihan_tanggal) != 2:
    st.info("Pilih tanggal awal dan akhir.")
    st.stop()

awal, akhir = pilihan_tanggal

data = data[
    (data["Tanggal"].dt.date >= awal)
    & (data["Tanggal"].dt.date <= akhir)
].copy()

if data.empty:
    st.warning("Tidak ada data untuk filter yang dipilih.")
    st.stop()

periode = (
    f"{awal.strftime('%d/%m/%Y')}–"
    f"{akhir.strftime('%d/%m/%Y')}"
)

st.caption(
    f"Periode terpilih: {periode} | "
    f"{angka(len(data))} dari {angka(len(df))} baris."
)


total_omzet = data["Omzet_Bersih_Rp"].sum()
total_transaksi = data["Jumlah_Transaksi"].sum()

rata_transaksi = (
    total_omzet / total_transaksi
    if total_transaksi > 0 else 0
)

valid = data[
    (data["Jumlah_Ulasan"] > 0)
    & data["Rating_Rata_rata"].notna()
].copy()

total_ulasan = valid["Jumlah_Ulasan"].sum()

rating_total = (
    (
        valid["Rating_Rata_rata"]
        * valid["Jumlah_Ulasan"]
    ).sum() / total_ulasan
    if total_ulasan > 0 else None
)

st.subheader("Ringkasan Kinerja")

k1, k2, k3, k4 = st.columns(4)

with k1:
    kartu(
        "Total Omzet Bersih",
        ringkas(total_omzet),
        rupiah(total_omzet)
    )

with k2:
    kartu(
        "Total Transaksi",
        angka(total_transaksi),
        "Transaksi periode terpilih"
    )

with k3:
    kartu(
        "Rata-rata Nilai Transaksi",
        rupiah(rata_transaksi),
        "Omzet bersih ÷ transaksi"
    )

with k4:
    kartu(
        "Rating Pelanggan",
        (
            skor(rating_total) + " / 5"
            if rating_total is not None else "N/A"
        ),
        "Rata-rata berbobot jumlah ulasan"
    )




outlet = (
    data.groupby("Outlet")["Omzet_Bersih_Rp"]
    .sum()
    .sort_values()
)

kanal = (
    data.groupby("Kanal_Penjualan")[
        "Omzet_Bersih_Rp"
    ]
    .sum()
    .sort_values()
)

harian_outlet = (
    data.groupby(
        ["Tanggal", "Outlet"],
        as_index=False
    )[["Omzet_Bersih_Rp", "Jumlah_Transaksi"]]
    .sum()
)

harian = (
    data.groupby("Tanggal", as_index=False)[
        "Omzet_Bersih_Rp"
    ]
    .sum()
    .sort_values("Tanggal")
)

bulanan = (
    data.groupby(
        pd.Grouper(key="Tanggal", freq="MS")
    )["Omzet_Bersih_Rp"]
    .sum()
    .reset_index()
)

bulanan = bulanan[
    bulanan["Tanggal"].dt.to_period("M").isin(
        data["Tanggal"].dt.to_period("M").unique()
    )
].copy()


tab1, tab2 = st.tabs(["📊 Ringkasan Bisnis", "🔍 Analisis Mendalam"])

with tab1:
    kiri_atas, kanan_atas = st.columns(2, gap="medium")
    with kiri_atas:
        st.subheader("Perbandingan Omzet Bersih Outlet")

        outlet_utama = outlet.idxmax()
        kontribusi_outlet = (
            outlet.max() / total_omzet * 100
            if total_omzet > 0 else 0
        )

        insight(
            f"{outlet_utama} menyumbang "
            f"{persen(kontribusi_outlet)} "
            "dari total omzet bersih pada "
            "filter yang dipilih."
        )

        fig1a = go.Figure()

        persen_outlet = (
            outlet / total_omzet * 100
            if total_omzet > 0 else outlet * 0
        )

        fig1a.add_trace(go.Bar(
            x=outlet / 1_000_000_000,
            y=outlet.index,
            orientation="h",
            marker_color=[
                COKELAT if o == outlet_utama else ABU
                for o in outlet.index
            ],
            text=[
                f"Rp {v:.2f} M"
                for v in outlet / 1_000_000_000
            ],
            textposition="outside",
            customdata=np.column_stack((
                outlet.values,
                persen_outlet.values
            )),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Omzet: Rp%{customdata[0]:,.0f}<br>"
                "Kontribusi: %{customdata[1]:.2f}%"
                "<extra></extra>"
            )
        ))

        fig1a.update_layout(
            xaxis_title="Omzet bersih (miliar rupiah)",
            yaxis_title="",
            showlegend=False
        )
        fig1a.update_xaxes(
            range=[
                0,
                max(outlet.max() / 1_000_000_000 * 1.4, 0.1)
            ],
            showgrid=False
        )

        gaya(fig1a)
        tampil(fig1a, "fig1a")



    with kanan_atas:
        st.subheader("Perbandingan Omzet Kanal Penjualan")

        kanal_utama = kanal.idxmax()
        kontribusi_kanal = (
            kanal.max() / total_omzet * 100
            if total_omzet > 0 else 0
        )

        insight(
            f"Kanal {kanal_utama} menyumbang "
            f"{persen(kontribusi_kanal)} "
            "dari total omzet bersih pada "
            "filter yang dipilih."
        )

        fig1b = go.Figure()

        persen_kanal = (
            kanal / total_omzet * 100
            if total_omzet > 0 else kanal * 0
        )

        fig1b.add_trace(go.Scatter(
            x=kanal / 1_000_000_000,
            y=kanal.index,
            mode="markers+text",
            marker=dict(
                size=17,
                color=[
                    COKELAT if k == kanal_utama
                    else "#9DA7B1"
                    for k in kanal.index
                ]
            ),
            text=[
                f"Rp {v:.2f} M"
                for v in kanal / 1_000_000_000
            ],
            textposition="middle right",
            customdata=np.column_stack((
                kanal.values,
                persen_kanal.values
            )),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Omzet: Rp%{customdata[0]:,.0f}<br>"
                "Kontribusi: %{customdata[1]:.2f}%"
                "<extra></extra>"
            )
        ))

        fig1b.update_layout(
            xaxis_title="Omzet bersih (miliar rupiah)",
            yaxis_title="",
            showlegend=False
        )
        fig1b.update_xaxes(
            range=[
                0,
                max(kanal.max() / 1_000_000_000 * 1.45, 0.1)
            ]
        )

        gaya(fig1b)
        tampil(fig1b, "fig1b")



    kiri_bawah, kanan_bawah = st.columns(2, gap="medium")
    with kiri_bawah:
        st.subheader("Proporsi Omzet Produk Sebelum Diskon")

        omzet_gudeg = data["Omzet_Gudeg_Rp"].sum()
        omzet_oleh = data["Omzet_Oleh_Oleh_Rp"].sum()
        total_produk = omzet_gudeg + omzet_oleh

        if total_produk > 0:
            pg = omzet_gudeg / total_produk * 100
            po = omzet_oleh / total_produk * 100

            produk_utama = (
                "Gudeg" if omzet_gudeg > omzet_oleh
                else "Oleh-oleh" if omzet_oleh > omzet_gudeg
                else None
            )

            if produk_utama:
                insight(
                    f"{produk_utama} memberikan kontribusi "
                    f"omzet sebelum diskon terbesar "
                    f"({persen(max(pg, po))}). "
                    f"Total omzet produk adalah "
                    f"{rupiah(total_produk)}."
                )
            else:
                insight(
                    "Gudeg dan Oleh-oleh memiliki "
                    "kontribusi omzet sebelum diskon "
                    "yang sama."
                )

            fig3 = go.Figure()

            for nama, nilai, bagian, warna in [
                ("Gudeg", omzet_gudeg, pg, COKELAT),
                ("Oleh-oleh", omzet_oleh, po, HIJAU)
            ]:
                fig3.add_trace(go.Bar(
                    x=[bagian],
                    y=["Total Usaha"],
                    orientation="h",
                    name=nama,
                    marker_color=warna,
                    text=[persen(bagian)],
                    textposition="inside",
                    textfont=dict(color="white", size=15),
                    customdata=[[nilai]],
                    hovertemplate=(
                        f"<b>{nama}</b><br>"
                        "Kontribusi: %{x:.2f}%<br>"
                        "Omzet: Rp%{customdata[0]:,.0f}"
                        "<extra></extra>"
                    )
                ))

            fig3.update_layout(
                barmode="stack",
                xaxis=dict(
                    title="Kontribusi omzet (%)",
                    range=[0, 100],
                    ticksuffix="%",
                    showgrid=False
                ),
                yaxis_title="",
                legend=dict(
                    orientation="h",
                    x=0.5,
                    xanchor="center",
                    y=1.2
                )
            )

            gaya(fig3, 300)
            tampil(fig3, "fig3")
            st.caption(
                "Proporsi menggunakan omzet produk sebelum "
                "diskon, bukan omzet bersih."
            )
        else:
            st.info("Tidak ada omzet produk pada filter ini.")



    with kanan_bawah:
        st.subheader("Tren Omzet Bersih Bulanan")

        bulan_tertinggi = bulanan.loc[
            bulanan["Omzet_Bersih_Rp"].idxmax()
        ]
        bulan_terendah = bulanan.loc[
            bulanan["Omzet_Bersih_Rp"].idxmin()
        ]

        nama_tinggi = BULAN[
            bulan_tertinggi["Tanggal"].month - 1
        ]
        nama_rendah = BULAN[
            bulan_terendah["Tanggal"].month - 1
        ]

        insight(
            f"Omzet bulanan tertinggi pada data terpilih "
            f"terjadi pada {nama_tinggi} "
            f"({rupiah(bulan_tertinggi['Omzet_Bersih_Rp'])}), "
            f"sedangkan yang terendah pada {nama_rendah} "
            f"({rupiah(bulan_terendah['Omzet_Bersih_Rp'])})."
        )

        fig5a = go.Figure()

        fig5a.add_trace(go.Scatter(
            x=bulanan["Tanggal"],
            y=bulanan["Omzet_Bersih_Rp"] / 1_000_000_000,
            mode="lines+markers",
            line=dict(color=COKELAT, width=3),
            marker=dict(size=8),
            customdata=bulanan[
                ["Omzet_Bersih_Rp"]
            ].to_numpy(),
            hovertemplate=(
                "<b>%{x|%b %Y}</b><br>"
                "Omzet: Rp%{customdata[0]:,.0f}"
                "<extra></extra>"
            ),
            showlegend=False
        ))

        fig5a.add_trace(go.Scatter(
            x=[
                bulan_tertinggi["Tanggal"],
                bulan_terendah["Tanggal"]
            ],
            y=[
                bulan_tertinggi["Omzet_Bersih_Rp"] / 1e9,
                bulan_terendah["Omzet_Bersih_Rp"] / 1e9
            ],
            mode="markers",
            marker=dict(
                color=[HIJAU, "#B45B4C"],
                size=13,
                line=dict(color="white", width=2)
            ),
            showlegend=False,
            hoverinfo="skip"
        ))

        fig5a.update_layout(
            xaxis_title="Bulan",
            yaxis_title="Omzet bersih (miliar rupiah)"
        )
        fig5a.update_xaxes(
            tickformat="%b %Y",
            dtick="M1",
            showgrid=False
        )

        gaya(fig5a)
        tampil(fig5a, "fig5a")


with tab2:
    kiri_atas, kanan_atas = st.columns(2, gap="medium")
    with kiri_atas:
        st.subheader("Distribusi Omzet Harian per Outlet")

        boxdata = harian_outlet.copy()
        boxdata["Juta"] = (
            boxdata["Omzet_Bersih_Rp"] / 1_000_000
        )

        median = (
            boxdata.groupby("Outlet")["Juta"]
            .median()
            .sort_values(ascending=False)
        )

        insight(
            f"{median.idxmax()} memiliki median omzet "
            f"harian tertinggi sebesar "
            f"Rp {skor(median.max())} juta "
            "pada periode terpilih."
        )

        fig2 = go.Figure()

        for nama in median.index:
            bagian = boxdata[boxdata["Outlet"] == nama]

            fig2.add_trace(go.Box(
                x=[nama] * len(bagian),
                y=bagian["Juta"],
                name=nama,
                marker_color=WARNA_OUTLET.get(nama, ABU),
                boxpoints="outliers",
                showlegend=False,
                hovertemplate=(
                    f"<b>{nama}</b><br>"
                    "Omzet harian: Rp%{y:.2f} juta"
                    "<extra></extra>"
                )
            ))

        fig2.update_layout(
            xaxis_title="Outlet",
            yaxis_title="Omzet harian (juta rupiah)"
        )
        gaya(fig2, 480)
        tampil(fig2, "fig2")



    with kanan_atas:
        st.subheader("Transaksi vs Omzet Bersih Harian")

        scatter = harian_outlet.copy()
        scatter["Juta"] = (
            scatter["Omzet_Bersih_Rp"] / 1_000_000
        )
        scatter["Tanggal_Label"] = (
            scatter["Tanggal"].dt.strftime("%d-%m-%Y")
        )

        r = scatter[
            ["Jumlah_Transaksi", "Juta"]
        ].corr().iloc[0, 1]

        if pd.notna(r):
            arah = (
                "positif" if r > 0
                else "negatif" if r < 0
                else "mendekati nol"
            )
            insight(
                f"Korelasi Pearson antara jumlah transaksi "
                f"harian dan omzet bersih adalah "
                f"{skor(r)} ({arah}). "
                "Korelasi ini menunjukkan hubungan, "
                "bukan bukti sebab-akibat."
            )
        else:
            insight(
                "Korelasi tidak dapat dihitung secara "
                "andal pada pilihan data ini."
            )

        fig4 = go.Figure()

        for nama in scatter["Outlet"].unique():
            bagian = scatter[
                scatter["Outlet"] == nama
            ]

            fig4.add_trace(go.Scatter(
                x=bagian["Jumlah_Transaksi"],
                y=bagian["Juta"],
                mode="markers",
                name=nama,
                marker=dict(
                    color=WARNA_OUTLET.get(nama, ABU),
                    size=7,
                    opacity=0.6
                ),
                customdata=bagian[
                    ["Tanggal_Label"]
                ].to_numpy(),
                hovertemplate=(
                    f"<b>{nama}</b><br>"
                    "Tanggal: %{customdata[0]}<br>"
                    "Transaksi: %{x:,.0f}<br>"
                    "Omzet: Rp%{y:.2f} juta"
                    "<extra></extra>"
                )
            ))

        fig4.update_layout(
            xaxis_title="Jumlah transaksi harian",
            yaxis_title="Omzet harian (juta rupiah)",
            legend=dict(
                orientation="h",
                x=0.5,
                xanchor="center",
                y=1.13
            )
        )

        gaya(fig4, 490)
        tampil(fig4, "fig4")



    kiri_bawah, kanan_bawah = st.columns(2, gap="medium")
    with kiri_bawah:
        st.subheader(
            "Omzet Harian dan Rata-rata Bergerak 7 Hari"
        )

        ma = harian.copy()
        ma["Juta"] = ma["Omzet_Bersih_Rp"] / 1e6

        # Reindex ke tanggal kalender agar jendela
        # benar-benar mewakili tujuh hari.
        kalender = pd.date_range(
            start=awal,
            end=akhir,
            freq="D"
        )

        ma = (
            ma.set_index("Tanggal")
            .reindex(kalender)
            .rename_axis("Tanggal")
            .reset_index()
        )

        ma["MA7"] = (
            ma["Omzet_Bersih_Rp"]
            .rolling(window=7, min_periods=7)
            .mean() / 1e6
        )

        valid_ma = ma.dropna(subset=["MA7"])

        if not valid_ma.empty:
            puncak = valid_ma.loc[
                valid_ma["MA7"].idxmax()
            ]

            insight(
                "Rata-rata omzet bersih 7 hari mencapai "
                f"puncak {rupiah(puncak['MA7'] * 1e6)} "
                "per hari, untuk periode yang berakhir "
                f"{puncak['Tanggal'].strftime('%d/%m/%Y')}."
            )
        else:
            insight(
                "Rata-rata bergerak 7 hari belum tersedia "
                "karena periode terpilih belum mencakup "
                "tujuh hari kalender dengan data lengkap."
            )

        fig5b = go.Figure()

        fig5b.add_trace(go.Scatter(
            x=ma["Tanggal"],
            y=ma["Juta"],
            mode="lines",
            name="Omzet harian",
            line=dict(color="#C6CDD5", width=1.2)
        ))

        fig5b.add_trace(go.Scatter(
            x=ma["Tanggal"],
            y=ma["MA7"],
            mode="lines",
            name="Rata-rata bergerak 7 hari",
            line=dict(color=COKELAT, width=3.2)
        ))

        if not valid_ma.empty:
            fig5b.add_trace(go.Scatter(
                x=[puncak["Tanggal"]],
                y=[puncak["MA7"]],
                mode="markers",
                marker=dict(
                    color=COKELAT,
                    size=12,
                    line=dict(color="white", width=2)
                ),
                showlegend=False,
                hovertemplate=(
                    "Puncak MA 7 hari<br>"
                    "%{x|%d %b %Y}<br>"
                    "Rp%{y:.2f} juta"
                    "<extra></extra>"
                )
            ))

        fig5b.update_layout(
            xaxis_title="Tanggal",
            yaxis_title="Omzet harian (juta rupiah)",
            hovermode="x unified",
            legend=dict(
                orientation="h",
                x=0.5,
                xanchor="center",
                y=1.13
            )
        )

        gaya(fig5b, 490)
        tampil(fig5b, "fig5b")



    with kanan_bawah:
        st.subheader("Rating Pelanggan per Outlet")

        if not valid.empty:
            rating = valid.copy()

            rating["Skor"] = (
                rating["Rating_Rata_rata"]
                * rating["Jumlah_Ulasan"]
            )

            rating = rating.groupby("Outlet").agg(
                Skor=("Skor", "sum"),
                Ulasan=("Jumlah_Ulasan", "sum")
            )

            rating["Nilai"] = (
                rating["Skor"] / rating["Ulasan"]
            )

            rating = rating.sort_values("Nilai")

            tertinggi = rating["Nilai"].idxmax()
            terendah = rating["Nilai"].idxmin()

            if tertinggi != terendah:
                teks_rating = (
                    f"{tertinggi} memiliki rating tertinggi "
                    f"({skor(rating.loc[tertinggi, 'Nilai'])}/5), "
                    f"sedangkan {terendah} terendah "
                    f"({skor(rating.loc[terendah, 'Nilai'])}/5) "
                    "pada pilihan filter."
                )
            else:
                teks_rating = (
                    f"Rating berbobot {tertinggi} adalah "
                    f"{skor(rating.loc[tertinggi, 'Nilai'])}/5 "
                    "pada pilihan filter."
                )

            insight(teks_rating)

            fig6 = go.Figure()

            fig6.add_trace(go.Bar(
                x=rating["Nilai"],
                y=rating.index,
                orientation="h",
                marker_color=[
                    COKELAT if o == terendah else "#AEB9C4"
                    for o in rating.index
                ],
                text=[
                    skor(v) for v in rating["Nilai"]
                ],
                textposition="outside",
                customdata=rating[["Ulasan"]].to_numpy(),
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Rating: %{x:.2f}/5<br>"
                    "Ulasan: %{customdata[0]:,.0f}"
                    "<extra></extra>"
                )
            ))

            fig6.update_layout(
                xaxis_title="Rating berbobot (0–5)",
                yaxis_title="",
                showlegend=False
            )
            fig6.update_xaxes(
                range=[0, 5.15],
                dtick=1,
                showgrid=False
            )

            gaya(fig6, 430)
            tampil(fig6, "fig6")

        else:
            st.info("Tidak ada data rating yang valid.")





with st.expander("Petunjuk Penggunaan Dashboard"):
    st.markdown("""
    1. Pilih outlet, kanal penjualan, dan rentang tanggal.
    2. Perhatikan perubahan empat KPI.
    3. Buka kedua tab untuk melihat delapan grafik.
    4. Baca kalimat temuan utama di atas setiap grafik.
    5. Arahkan kursor ke grafik untuk melihat rincian.
    """)

st.caption(
    "Gudeg Sekar Arum 2025 | "
    "Sumber: Data simulasi penjualan | "
    "Dataset: 1 Januari–31 Desember 2025."
)
