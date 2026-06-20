import streamlit as st
import pandas as pd

from processing import (
    procesar_datos,
    obtener_metricas,
)
from viz import (
    plot_titles_by_type,
    plot_top_genres,
    plot_titles_by_year,
    plot_top_countries,
    plot_rating_distribution,
)
from db import (
    consultar_catalogo_enriquecido,
    consultar_top_imdb,
    obtener_metricas_db,
    obtener_metricas_omdb,
)
from api_or_scraper import buscar_titulo_omdb_inteligente


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

  .stApp {
      background: #0a0a0a;
      color: #e8e8e8;
  }

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

  [data-testid="stSelectbox"] > div > div {
      background: #1a1a1a !important;
      border: 1px solid #333 !important;
      border-radius: 6px !important;
      color: #e8e8e8 !important;
  }

  [data-testid="stSlider"] .stSlider > div {
      color: #E50914 !important;
  }
  [data-testid="stSlider"] [data-baseweb="slider"] [data-testid="stThumbValue"] {
      color: #E50914 !important;
  }

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

  p, .stMarkdown p {
      font-family: 'DM Sans', sans-serif !important;
      color: #999999 !important;
      font-size: 0.95rem;
  }

  .stCaption {
      color: #555555 !important;
      font-family: 'DM Sans', sans-serif !important;
  }

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

  hr {
      border-color: #1e1e1e !important;
  }

  [data-testid="stPlotlyChart"],
  .stPlot {
      background: #111111 !important;
      border-radius: 12px !important;
      border: 1px solid #222222 !important;
      padding: 0.5rem;
  }

  #MainMenu {visibility: hidden;}
  footer {visibility: hidden;}

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
  Explora el catálogo completo de Netflix con filtros interactivos, métricas, visualizaciones
  y datos enriquecidos desde IMDb.
</p>
""", unsafe_allow_html=True)
st.caption("Fuente del dataset: Netflix Titles / Kaggle. Datos externos: OMDb API (IMDb).")

st.markdown("""<hr style="border:none; border-top:1px solid #1e1e1e; margin:0.5rem 0 1.5rem;">""", unsafe_allow_html=True)


# ── Carga de datos (CSV procesado, para filtros y gráficos de Netflix) ──────

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
  Netflix Dashboard · Datos Kaggle + OMDb
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


# ── Métricas (Netflix) ───────────────────────────────────────────────────────

st.markdown("""
<div style="font-family:'Bebas Neue',sans-serif; font-size:1.3rem; letter-spacing:0.1em; color:#E50914; margin-bottom:0.8rem;">
  ● MÉTRICAS DESCRIPTIVAS
</div>
""", unsafe_allow_html=True)

metricas = obtener_metricas(df_filtered)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total de títulos",    metricas["total_titulos"])
col2.metric("Películas",           metricas["total_peliculas"])
col3.metric("Series",              metricas["total_series"])
col4.metric("Países distintos",    metricas["total_paises"])
col5.metric("Géneros distintos",   metricas["total_generos"])

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


# ── Visualizaciones (Netflix) ────────────────────────────────────────────────

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


# ── Top 10 títulos más recientes (Netflix) ───────────────────────────────────

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

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""<hr style="border:none; border-top:1px solid #1e1e1e; margin:1rem 0 1.5rem;">""", unsafe_allow_html=True)


# ── Datos enriquecidos con OMDb / IMDb (desde SQLite) ────────────────────────

st.markdown("""
<div style="font-family:'Bebas Neue',sans-serif; font-size:1.3rem; letter-spacing:0.1em; color:#E50914; margin-bottom:0.8rem;">
  ● DATOS ENRIQUECIDOS CON OMDb / IMDb
</div>
""", unsafe_allow_html=True)

try:
    df_enriquecido = consultar_catalogo_enriquecido()
    metricas_db = obtener_metricas_db()
    metricas_omdb = obtener_metricas_omdb()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Títulos enriquecidos",
        int(metricas_omdb["enriched_titles"])
        if metricas_omdb["enriched_titles"] else 0
    )

    col2.metric(
        "IMDb promedio",
        metricas_omdb["average_imdb_rating"]
        if metricas_omdb["average_imdb_rating"] else "—"
    )

    col3.metric(
        "IMDb máximo",
        metricas_omdb["maximum_imdb_rating"]
        if metricas_omdb["maximum_imdb_rating"] else "—"
    )

    col4.metric(
        "Total votos IMDb",
        int(metricas_omdb["total_imdb_votes"])
        if metricas_omdb["total_imdb_votes"] else 0
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### Top 10 títulos según IMDb")

    top_imdb = consultar_top_imdb(limite=10, minimo_votos=1000)

    st.dataframe(
        top_imdb,
        use_container_width=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### Catálogo enriquecido")

    columnas_enriquecido = [
        "title",
        "type",
        "release_year",
        "main_genre",
        "imdb_rating",
        "imdb_votes",
        "source",
    ]

    st.dataframe(
        df_enriquecido[columnas_enriquecido],
        use_container_width=True,
        height=350,
    )

except Exception as e:
    st.warning(
        "No se pudo cargar la base SQLite. "
        "Ejecuta primero: python3 src/build_database.py"
    )
    st.code(str(e))

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""<hr style="border:none; border-top:1px solid #1e1e1e; margin:1rem 0 1.5rem;">""", unsafe_allow_html=True)


# ── Búsqueda en vivo en OMDb ──────────────────────────────────────────────────

st.markdown("""
<div style="font-family:'Bebas Neue',sans-serif; font-size:1.3rem; letter-spacing:0.1em; color:#E50914; margin-bottom:0.8rem;">
  ● BÚSQUEDA EN VIVO EN OMDb
</div>
""", unsafe_allow_html=True)

st.markdown("""
<p style="color:#777; font-size:0.85rem; margin-top:-8px;">
  Busca cualquier título directamente en la API de OMDb, sin necesidad de que esté en el catálogo.
</p>
""", unsafe_allow_html=True)

col_a, col_b, col_c = st.columns([3, 1.5, 1])

with col_a:
    titulo_busqueda = st.text_input("Título a buscar")

with col_b:
    tipo_busqueda = st.selectbox("Tipo", ["Movie", "TV Show"])

with col_c:
    anio_busqueda = st.number_input(
        "Año",
        min_value=1900,
        max_value=2030,
        value=2016,
    )

if st.button("Buscar en vivo"):
    if not titulo_busqueda:
        st.warning("Escribe un título antes de buscar.")
    else:
        with st.spinner("Consultando OMDb..."):
            resultado = buscar_titulo_omdb_inteligente(
                titulo=titulo_busqueda,
                tipo=tipo_busqueda,
                anio=anio_busqueda,
            )

        if resultado:
            col_img, col_info = st.columns([1, 2])

            with col_img:
                poster = resultado.get("poster_omdb")
                if poster:
                    st.image(poster)

            with col_info:
                st.markdown(f"**Título OMDb:** {resultado.get('title_omdb')}")
                st.markdown(f"**Año:** {resultado.get('year_omdb')}")
                st.markdown(f"**IMDb rating:** {resultado.get('imdb_rating')}")
                st.markdown(f"**IMDb votos:** {resultado.get('imdb_votes')}")
                st.markdown(f"**Género:** {resultado.get('genre_omdb')}")
                st.markdown(f"**Director:** {resultado.get('director_omdb')}")
                st.markdown(f"**Método de coincidencia:** {resultado.get('match_method')}")
                st.markdown(f"**Similitud:** {resultado.get('similarity_score')}")
                st.markdown(f"**Sinopsis:** {resultado.get('plot_omdb')}")
        else:
            st.error("No se encontró el título en OMDb.")
