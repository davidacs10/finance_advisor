# src/app.py
import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from logic.loader import cargar_excel

# ── Configuración de página ──────────────────────────────
st.set_page_config(page_title="AI Finance Advisor", page_icon="💰", layout="wide")

st.title("💰 AI Finance Advisor")
st.caption("Sube tu reporte de gastos en Excel y obtén análisis personalizados.")

# ── Upload ───────────────────────────────────────────────
archivo = st.file_uploader(
    "Sube tu archivo de gastos",
    type=["xlsx"],
    help="El archivo debe tener columnas: Fecha, Concepto, Monto, Categoria",
)

if archivo is None:
    st.info("👆 Sube un archivo .xlsx para comenzar.")
    st.stop()

# ── Carga y validación ───────────────────────────────────
df, error = cargar_excel(archivo)

if error:
    st.error(f"❌ {error}")
    st.stop()

st.success(f"✅ Archivo cargado: **{len(df)} registros** encontrados.")

# ── Métricas resumen ─────────────────────────────────────
col1, col2, col3 = st.columns(3)
col1.metric("Total gastado", f"${df['Monto'].sum():,.2f}")
col2.metric("Gasto promedio", f"${df['Monto'].mean():,.2f}")
col3.metric("Categorías", df["Categoria"].nunique())

# ── Vista previa de datos ────────────────────────────────
st.subheader("Vista previa")

categorias = ["Todas"] + sorted(df["Categoria"].unique().tolist())
filtro = st.selectbox("Filtrar por categoría", categorias)

df_vista = df if filtro == "Todas" else df[df["Categoria"] == filtro]
st.dataframe(df_vista, use_container_width=True, hide_index=True)
