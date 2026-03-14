# 🤖 AI Finance Advisor (Gestor de Finanzas con IA)

Un asistente inteligente de finanzas personales desarrollado en **Python** que analiza tus reportes de gastos en Excel y utiliza Inteligencia Artificial para ofrecerte consejos de ahorro personalizados.

---

## 🚀 Funcionalidades

- **Carga de Datos:** Sube archivos `.xlsx` de forma sencilla.
- **Dashboard Interactivo:** Visualización de gastos por categorías mediante gráficos de pastel y barras.
- **Análisis con IA:** Conexión con modelos de lenguaje (GPT/Gemini) para detectar "gastos hormiga" y sugerir planes de ahorro.
- **Resumen Estadístico:** Cálculo automático de totales, promedios y variaciones mensuales.

## 🛠️ Stack Tecnológico

- **Frontend:** [Streamlit](https://streamlit.io/)
- **Procesamiento de Datos:** [Pandas](https://pandas.pydata.org/)
- **Gráficos:** [Plotly](https://plotly.com/python/)
- **IA:** OpenAI API / LangChain

## 📂 Estructura del Proyecto

```text
.
├── src/
│   ├── app.py              # Interfaz de usuario (Streamlit)
│   ├── logic/              # Procesamiento de datos (Pandas)
│   └── ai/                 # Lógica de prompts e IA
├── data/                   # Archivos de ejemplo
├── .env                    # Variables de entorno (API Keys)
└── requirements.txt        # Dependencias del proyecto
```

## ⚙️ Instalación y Configuración

1. **Clonar el repositorio:**

```bash
git clone [https://github.com/tu-usuario/mi-proyecto-finanzas.git](https://github.com/tu-usuario/mi-proyecto-finanzas.git)
cd mi-proyecto-finanzas

```

2. **Crear y activar entorno virtual:**

```bash
python -m venv venv
# En Windows:
.\venv\Scripts\activate
# En Mac/Linux:
source venv/bin/activate

```

3. **Instalar dependencias:**

```bash
pip install -r requirements.txt

```

4. **Configurar API Key:**
   Crea un archivo `.env` en la raíz y añade tu llave:

```env
OPENAI_API_KEY=tu_api_key_aqui

```

5. **Ejecutar la aplicación:**

```bash
streamlit run src/app.py

```

## 📊 Formato del Excel Sugerido

Para que la app funcione correctamente, el archivo Excel debe contener las siguientes columnas:

- `Fecha`: (DD/MM/AAAA)
- `Concepto`: Descripción del gasto.
- `Monto`: Valor numérico del gasto.
- `Categoria`: (Ej: Comida, Transporte, Vivienda, Ocio).

---

Desarrollado con ❤️ por [[David](https://github.com/davidacs10)]
