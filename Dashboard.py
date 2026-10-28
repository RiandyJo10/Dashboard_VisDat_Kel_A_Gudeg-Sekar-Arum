
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

[data-testid="stSelectbox"] [data-baseweb="select"] > div,
[data-testid="stSelectbox"] [data-baseweb="select"],
[data-testid="stDateInput"] [data-baseweb="input"],
[data-testid="stDateInput"] [data-baseweb="base-input"],
[data-testid="stDateInputField"] [data-baseweb="input"],
[data-testid="stDateInputField"] [data-baseweb="base-input"] {
    background: linear-gradient(110deg, #5B392B, #A9673F) !important;
    background-color: #5B392B !important;
    border: 1px solid #A9673F !important;
    border-radius: 12px !important;
    color: #FFFFFF !important;
    min-height: 46px;
}

[data-testid="stSelectbox"] [data-baseweb="select"] > div > div,
[data-testid="stDateInput"] [data-baseweb="input"] > div,
[data-testid="stDateInput"] [data-baseweb="base-input"] > div,
[data-testid="stDateInputField"] [data-baseweb="input"] > div {
    background: transparent !important;
}

[data-testid="stSelectbox"] [data-baseweb="select"] *,
[data-testid="stDateInput"] [data-baseweb="input"] *,
[data-testid="stDateInput"] [data-baseweb="base-input"] *,
[data-testid="stDateInputField"] [data-baseweb="input"] * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}
[data-testid="stSelectbox"] svg,
[data-testid="stDateInput"] svg,
[data-testid="stDateInputField"] svg {
    color: #FFFFFF !important;
    fill: none !important;
    stroke: #FFFFFF !important;
}
[data-testid="stDateInput"] input,
[data-testid="stDateInputField"] input {
    background: transparent !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}
[data-testid="stSelectbox"] [data-baseweb="select"] > div:focus-within,
[data-testid="stDateInput"] [data-baseweb="input"]:focus-within {
    border-color: #E6C39D !important;
    box-shadow: 0 0 0 2px rgba(169, 103, 63, 0.2) !important;
}
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
