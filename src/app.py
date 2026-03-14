# src/app.py
import streamlit as st
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from logic.loader import cargar_excel
from logic.analyzer import resumen_por_categoria, variacion_mensual
from logic.charts import grafico_pastel, grafico_barras_mes, grafico_barras_categoria
from logic.ai_advisor import analizar_gastos

st.set_page_config(page_title="AI Finance Advisor", page_icon="💰", layout="wide")
st.title("💰 AI Finance Advisor")
st.caption("Sube tu reporte de gastos en Excel y obtén análisis personalizados.")

# ── Ejemplo de formato esperado ──────────────────────────
with st.expander("📋 ¿Cómo debe estructurarse el archivo Excel?"):
    st.markdown("Tu archivo `.xlsx` debe tener **exactamente estas 4 columnas:**")

    import pandas as pd

    df_ejemplo = pd.DataFrame(
        {
            "Fecha": [
                "05/01/2024",
                "12/01/2024",
                "18/01/2024",
                "03/02/2024",
                "15/02/2024",
            ],
            "Concepto": ["Supermercado", "Netflix", "Gasolina", "Restaurante", "Gym"],
            "Monto": [1200.00, 250.00, 800.00, 450.00, 350.00],
            "Categoria": ["Comida", "Ocio", "Transporte", "Comida", "Salud"],
        }
    )
    st.dataframe(df_ejemplo, use_container_width=True, hide_index=True)

    st.markdown("**Reglas importantes:**")
    st.markdown(
        """
- `Fecha` → formato DD/MM/AAAA
- `Concepto` → descripción libre del gasto
- `Monto` → número sin símbolos (no escribas `$1,200` sino `1200`)
- `Categoria` → texto libre, pero sé consistente (siempre `Comida`, no a veces `comida` o `COMIDA`)
    """
    )

    with open("data/gastos_ejemplo.xlsx", "rb") as f:
        st.download_button(
            label="⬇️ Descargar archivo de ejemplo",
            data=f,
            file_name="gastos_ejemplo.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

# ── Upload ───────────────────────────────────────────────
archivo = st.file_uploader("Sube tu archivo de gastos", type=["xlsx"])

if archivo is None:
    st.info("👆 Sube un archivo .xlsx para comenzar.")
    st.stop()

df, error = cargar_excel(archivo)
if error:
    st.error(f"❌ {error}")
    st.stop()

# ── Métricas ─────────────────────────────────────────────
st.success(f"✅ {len(df)} registros cargados.")
col1, col2, col3 = st.columns(3)
col1.metric("Total gastado", f"${df['Monto'].sum():,.2f}")
col2.metric("Gasto promedio", f"${df['Monto'].mean():,.2f}")
col3.metric("Categorías", df["Categoria"].nunique())

st.divider()

# ── Dashboard ────────────────────────────────────────────
st.subheader("📊 Dashboard")

df_cat = resumen_por_categoria(df)
df_mes = variacion_mensual(df)

# Fila 1: pastel + barras por categoría
col_a, col_b = st.columns(2)
with col_a:
    st.markdown("**Distribución por categoría**")
    st.plotly_chart(grafico_pastel(df_cat), use_container_width=True)
with col_b:
    st.markdown("**Gasto por categoría**")
    st.plotly_chart(grafico_barras_categoria(df_cat), use_container_width=True)

# Fila 2: evolución mensual
st.markdown("**Evolución mensual del gasto**")
st.plotly_chart(grafico_barras_mes(df_mes), use_container_width=True)

# ── Tabla variación mensual ──────────────────────────────
st.subheader("📅 Variación mes a mes")
st.dataframe(
    df_mes.style.format({"Total": "${:,.2f}", "Variacion_%": "{:+.1f}%"}),
    use_container_width=True,
    hide_index=True,
)

# ── Vista detalle ────────────────────────────────────────
st.subheader("🔍 Detalle de transacciones")
categorias = ["Todas"] + sorted(df["Categoria"].unique().tolist())
filtro = st.selectbox("Filtrar por categoría", categorias)
df_vista = df if filtro == "Todas" else df[df["Categoria"] == filtro]
st.dataframe(df_vista, use_container_width=True, hide_index=True)

# ── Análisis con IA ──────────────────────────────────────
st.divider()
st.subheader("🤖 Análisis con IA")
st.caption("Gemini analizará tus patrones de gasto y te dará consejos personalizados.")

if st.button("✨ Analizar mis gastos con Gemini", type="primary"):
    with st.spinner("Gemini está analizando tus gastos..."):
        try:
            analisis = analizar_gastos(df)
            st.success("¡Análisis completado!")
            st.markdown(analisis)
        except Exception as e:
            st.error(f"Error al conectar con Gemini: {e}")
            st.info(
                "Verifica que tu GOOGLE_API_KEY esté correctamente configurada en el archivo .env"
            )
