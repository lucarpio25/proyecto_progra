import streamlit as st
import pandas as pd

from processing import (
    procesar_datos,
    obtener_metricas,
    obtener_generos_expandido,
    obtener_paises_expandido,
)
from viz import (
    plot_titles_by_type,
    plot_top_genres,
    plot_titles_by_year,
    plot_top_countries,
    plot_rating_distribution,
)


# ── Configuración de página ──────────────────────────────────────────────────

st.set_page_config(
    page_title="Netflix Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ── CSS personalizado ────────────────────────────────────────────────────────

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&display=swap');

  /* Fondo general */
  .stApp {
      background: #0a0a0a;
      color: #e8e8e8;
  }

  /* Sidebar */
  [data-testid="stSidebar"] {
      background: #111111 !important;
      border-right: 1px solid #222222;
  }
  [data-testid="stSidebar"] .stSelectbox label,
  [data-testid="stSidebar"] .stSlider label,
  [data-testid="stSidebar"] p,
  [data-testid="stSidebar"] span {
      color: #aaaaaa !important;
      font-family: 'DM Sans', sans-serif !important;
      font-size: 0.82rem !important;
      letter-spacing: 0.03em;
      text-transform: uppercase;
  }
  [data-testid="stSidebar"] h1,
  [data-testid="stSidebar"] h2,
  [data-testid="stSidebar"] h3 {
      color: #E50914 !important;
      font-family: 'Bebas Neue', sans-serif !important;
      letter-spacing: 0.08em;
  }

  /* Selectbox */
  [data-testid="stSelectbox"] > div > div {
      background: #1a1a1a !important;
      border: 1px solid #333 !important;
      border-radius: 6px !important;
      color: #e8e8e8 !important;
  }

  /* Slider */
  [data-testid="stSlider"] .stSlider > div {
      color: #E50914 !important;
  }
  [data-testid="stSlider"] [data-baseweb="slider"] [data-testid="stThumbValue"] {
      color: #E50914 !important;
  }

  /* Título principal */
  h1 {
      font-family: 'Bebas Neue', sans-serif !important;
      font-size: 3.2rem !important;
      letter-spacing: 0.06em !important;
      color: #ffffff !important;
      background: linear-gradient(90deg, #ffffff 0%, #E50914 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      margin-bottom: 0 !important;
  }

  h2, h3 {
      font-family: 'Bebas Neue', sans-serif !important;
      letter-spacing: 0.05em !important;
      color: #ffffff !important;
  }

  /* Párrafos */
  p, .stMarkdown p {
      font-family: 'DM Sans', sans-serif !important;
      color: #999999 !important;
      font-size: 0.95rem;
  }

  /* Caption */
  .stCaption {
      color: #555555 !important;
      font-family: 'DM Sans', sans-serif !important;
  }

  /* Cards de métricas */
  [data-testid="stMetric"] {
      background: linear-gradient(135deg, #161616 0%, #1e1e1e 100%);
      border: 1px solid #2a2a2a;
      border-radius: 12px;
      padding: 1.2rem 1.4rem !important;
      position: relative;
      overflow: hidden;
      transition: border-color 0.2s ease;
  }
  [data-testid="stMetric"]:hover {
      border-color: #E50914;
  }
  [data-testid="stMetric"]::before {
      content: '';
      position: absolute;
      top: 0; left: 0;
      width: 3px; height: 100%;
      background: #E50914;
      border-radius: 12px 0 0 12px;
  }
  [data-testid="stMetricLabel"] {
      font-family: 'DM Sans', sans-serif !important;
      font-size: 0.72rem !important;
      text-transform: uppercase !important;
      letter-spacing: 0.1em !important;
      color: #777777 !important;
  }
  [data-testid="stMetricValue"] {
      font-family: 'Bebas Neue', sans-serif !important;
      font-size: 2.4rem !important;
      color: #ffffff !important;
      letter-spacing: 0.03em !important;
  }

  /* Dataframe */
  [data-testid="stDataFrame"] {
      border: 1px solid #222222 !important;
      border-radius: 10px !important;
      overflow: hidden;
  }
  [data-testid="stDataFrame"] table {
      background: #111111 !important;
  }
  [data-testid="stDataFrame"] thead th {
      background: #1a1a1a !important;
      color: #E50914 !important;
      font-family: 'DM Sans', sans-serif !important;
      font-size: 0.75rem !important;
      text-transform: uppercase !important;
      letter-spacing: 0.08em !important;
      border-bottom: 1px solid #2a2a2a !important;
  }
  [data-testid="stDataFrame"] tbody td {
      color: #cccccc !important;
      font-family: 'DM Sans', sans-serif !important;
      font-size: 0.85rem !important;
      border-color: #1e1e1e !important;
  }
  [data-testid="stDataFrame"] tbody tr:hover td {
      background: #1a1a1a !important;
  }

  /* Divisores */
  hr {
      border-color: #1e1e1e !important;
  }

  /* Plots con fondo oscuro */
  [data-testid="stPlotlyChart"],
  .stPlot {
      background: #111111 !important;
      border-radius: 12px !important;
      border: 1px solid #222222 !important;
      padding: 0.5rem;
  }

  /* Ocultar el menú de Streamlit y footer */
  #MainMenu {visibility: hidden;}
  footer {visibility: hidden;}

  /* Scrollbar elegante */
  ::-webkit-scrollbar { width: 5px; }
  ::-webkit-scrollbar-track { background: #0a0a0a; }
  ::-webkit-scrollbar-thumb { background: #333; border-radius: 10px; }
  ::-webkit-scrollbar-thumb:hover { background: #E50914; }
</style>
""", unsafe_allow_html=True)


# ── Header ───────────────────────────────────────────────────────────────────

col_logo, col_title = st.columns([1, 11])
with col_logo:
    st.markdown("""
    <div style="font-size:3.5rem; line-height:1; padding-top:4px;">🎬</div>
    """, unsafe_allow_html=True)
with col_title:
    st.title("Netflix Catalog Dashboard")

st.markdown("""
<p style="color:#666; font-size:0.9rem; margin-top:-10px; margin-bottom:4px;">
  Explora el catálogo completo de Netflix con filtros interactivos, métricas y visualizaciones.
</p>
""", unsafe_allow_html=True)
st.caption("Fuente del dataset: Netflix Titles / Kaggle")

st.markdown("""<hr style="border:none; border-top:1px solid #1e1e1e; margin:0.5rem 0 1.5rem;">""", unsafe_allow_html=True)


# ── Carga de datos ───────────────────────────────────────────────────────────

DATA_PATH = "data/netflix_titles.csv"

try:
    df_raw = pd.read_csv(DATA_PATH, engine="python", on_bad_lines="skip")
    df = procesar_datos(df_raw)
except Exception as e:
    st.error("❌ Error al cargar los datos.")
    st.code(str(e))
    st.stop()


# ── Sidebar: filtros ─────────────────────────────────────────────────────────

st.sidebar.markdown("""
<div style="padding: 0.4rem 0 1rem;">
  <span style="font-family:'Bebas Neue',sans-serif; font-size:1.6rem; color:#E50914; letter-spacing:0.1em;">
    🎛 FILTROS
  </span>
</div>
""", unsafe_allow_html=True)

tipos = sorted(df["type"].dropna().unique())
selected_type = st.sidebar.selectbox("Tipo de contenido", ["Todos"] + tipos)

ratings = sorted(df["rating"].dropna().unique())
selected_rating = st.sidebar.selectbox("Clasificación", ["Todos"] + ratings)

paises = sorted(df["main_country"].dropna().unique())
paises = [p for p in paises if p != "Sin información"]
selected_country = st.sidebar.selectbox("País", ["Todos"] + paises)

min_year = int(df["release_year"].min())
max_year = int(df["release_year"].max())
year_range = st.sidebar.slider(
    "Rango de años",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<p style="font-size:0.7rem; color:#444; text-align:center; font-family:'DM Sans',sans-serif;">
  Netflix Dashboard · Datos Kaggle
</p>
""", unsafe_allow_html=True)


# ── Aplicar filtros ──────────────────────────────────────────────────────────

df_filtered = df.copy()

if selected_type != "Todos":
    df_filtered = df_filtered[df_filtered["type"] == selected_type]

if selected_rating != "Todos":
    df_filtered = df_filtered[df_filtered["rating"] == selected_rating]

if selected_country != "Todos":
    df_filtered = df_filtered[df_filtered["main_country"] == selected_country]

df_filtered = df_filtered[
    (df_filtered["release_year"] >= year_range[0]) &
    (df_filtered["release_year"] <= year_range[1])
]


# ── Métricas ─────────────────────────────────────────────────────────────────

st.markdown("""
<div style="font-family:'Bebas Neue',sans-serif; font-size:1.3rem; letter-spacing:0.1em; color:#E50914; margin-bottom:0.8rem;">
  ● MÉTRICAS DESCRIPTIVAS
</div>
""", unsafe_allow_html=True)

metricas = obtener_metricas(df_filtered)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total de títulos",   metricas["total_titulos"])
col2.metric("Películas",        metricas["total_peliculas"])
col3.metric("Series",           metricas["total_series"])
col4.metric("Países distintos", metricas["total_paises"])
col5.metric("Géneros distintos",metricas["total_generos"])

st.markdown("<br>", unsafe_allow_html=True)


# ── Tabla de datos filtrados ─────────────────────────────────────────────────

st.markdown("""
<div style="font-family:'Bebas Neue',sans-serif; font-size:1.3rem; letter-spacing:0.1em; color:#E50914; margin-bottom:0.8rem;">
  ● DATOS FILTRADOS
</div>
""", unsafe_allow_html=True)

st.dataframe(
    df_filtered[[
        "title", "type", "main_country",
        "release_year", "rating",
        "duration", "main_genre", "date_added",
    ]],
    use_container_width=True,
    height=320,
)

st.markdown("<br>", unsafe_allow_html=True)


# ── Visualizaciones ──────────────────────────────────────────────────────────

st.markdown("""
<div style="font-family:'Bebas Neue',sans-serif; font-size:1.3rem; letter-spacing:0.1em; color:#E50914; margin-bottom:0.8rem;">
  ● VISUALIZACIONES
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="medium")
with col1:
    st.markdown('<div class="stPlot">', unsafe_allow_html=True)
    st.pyplot(plot_titles_by_type(df_filtered))
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="stPlot">', unsafe_allow_html=True)
    st.pyplot(plot_rating_distribution(df_filtered))
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col3, col4 = st.columns(2, gap="medium")
with col3:
    st.markdown('<div class="stPlot">', unsafe_allow_html=True)
    st.pyplot(plot_top_genres(df_filtered))
    st.markdown('</div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="stPlot">', unsafe_allow_html=True)
    st.pyplot(plot_top_countries(df_filtered))
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="stPlot">', unsafe_allow_html=True)
st.pyplot(plot_titles_by_year(df_filtered))
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ── Top 10 títulos más recientes ─────────────────────────────────────────────

st.markdown("""
<div style="font-family:'Bebas Neue',sans-serif; font-size:1.3rem; letter-spacing:0.1em; color:#E50914; margin-bottom:0.8rem;">
  ● TOP 10 TÍTULOS MÁS RECIENTES
</div>
""", unsafe_allow_html=True)

top_recientes = df_filtered.sort_values(by="release_year", ascending=False).head(10)

st.dataframe(
    top_recientes[[
        "title", "type", "release_year",
        "main_country", "rating",
        "main_genre", "duration",
    ]],
    use_container_width=True,
    height=380,
)
