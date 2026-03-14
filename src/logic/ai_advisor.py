import os
import google.generativeai as genai
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel(
    model_name="gemini-3.1-flash-lite-preview",
    system_instruction="""Eres un asesor financiero personal experto y empático.
Recibes un resumen de gastos de un usuario y debes:
1. Identificar los 'gastos hormiga' (pequeños gastos frecuentes que suman mucho).
2. Detectar categorías donde se gasta más de lo razonable.
3. Dar 3 consejos concretos y accionables para ahorrar. Cada consejo debe ser escrito con bullet points y acompañado de un emoji relevante.
4. Estimar cuánto podría ahorrar al mes si sigue tus consejos.
Usa un tono amigable, directo y motivador. Responde en español.

La respuesta que no sea en formato markdown, sino texto plano con emojis para hacerlo más ameno.""",
)


def construir_resumen(df: pd.DataFrame) -> str:
    """
    Convierte el DataFrame en texto estructurado para Gemini.
    """
    total = df["Monto"].sum()
    promedio = df["Monto"].mean()

    por_categoria = df.groupby("Categoria")["Monto"].sum().sort_values(ascending=False)

    por_mes = (
        df.assign(Mes=df["Fecha"].dt.to_period("M").astype(str))
        .groupby("Mes")["Monto"]
        .sum()
    )

    resumen = f"""
RESUMEN DE GASTOS PERSONALES
=============================
Total gastado: ${total:,.2f}
Gasto promedio por transacción: ${promedio:,.2f}
Número de transacciones: {len(df)}

GASTOS POR CATEGORÍA:
{por_categoria.to_string()}

GASTOS POR MES:
{por_mes.to_string()}

TRANSACCIONES DETALLADAS:
{df[['Fecha','Concepto','Monto','Categoria']].to_string(index=False)}
"""
    return resumen.strip()


def analizar_gastos(df: pd.DataFrame) -> str:
    """
    Envía el resumen financiero a Gemini y retorna su análisis.
    """
    resumen = construir_resumen(df)

    prompt = f"Analiza mis gastos y dame consejos personalizados:\n\n{resumen}"

    response = model.generate_content(prompt)

    return response.text
