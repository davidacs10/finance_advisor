import plotly.express as px
import pandas as pd

COLORES = px.colors.qualitative.Pastel


def grafico_pastel(df_categoria: pd.DataFrame) -> px.pie:
    """Distribución del gasto por categoría."""
    fig = px.pie(
        df_categoria,
        names="Categoria",
        values="Total",
        color_discrete_sequence=COLORES,
        hole=0.4,  # donut, más moderno que pastel sólido
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20))
    return fig


def grafico_barras_mes(df_mes: pd.DataFrame) -> px.bar:
    """Gasto total por mes en barras verticales."""
    fig = px.bar(
        df_mes,
        x="Mes",
        y="Total",
        text="Total",
        color_discrete_sequence=["#6C63FF"],
    )
    fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    fig.update_layout(
        xaxis_title="", yaxis_title="Monto ($)", margin=dict(t=40, b=20, l=20, r=20)
    )
    return fig


def grafico_barras_categoria(df_categoria: pd.DataFrame) -> px.bar:
    """Gasto por categoría en barras horizontales."""
    fig = px.bar(
        df_categoria,
        x="Total",
        y="Categoria",
        orientation="h",
        text="Total",
        color="Total",
        color_continuous_scale="Purples",
    )
    fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    fig.update_layout(
        coloraxis_showscale=False,
        xaxis_title="Monto ($)",
        yaxis_title="",
        margin=dict(t=20, b=20, l=20, r=20),
    )
    return fig
