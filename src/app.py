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
    page_title="Dashboard Netflix",
    layout="wide"
)


# ── Título y descripción ─────────────────────────────────────────────────────

st.title("Dashboard del Catálogo de Netflix")

st.write("""
Esta aplicación permite explorar el catálogo de Netflix mediante filtros
interactivos, métricas descriptivas, tablas y visualizaciones.
""")

st.caption("Fuente del dataset: Netflix Titles / Kaggle.")


# ── Carga de datos ───────────────────────────────────────────────────────────

DATA_PATH = "data/netflix_titles.csv"

try:
    df_raw = pd.read_csv(DATA_PATH, engine="python", on_bad_lines="skip")
    df = procesar_datos(df_raw)
except Exception as e:
    st.error("Ocurrió un error al cargar los datos.")
    st.write(e)
    st.stop()


# ── Sidebar: filtros ─────────────────────────────────────────────────────────

st.sidebar.header("Filtros")

# Filtro por tipo
tipos = sorted(df["type"].dropna().unique())
selected_type = st.sidebar.selectbox("Tipo de contenido", ["Todos"] + tipos)

# Filtro por clasificación
ratings = sorted(df["rating"].dropna().unique())
selected_rating = st.sidebar.selectbox("Clasificación", ["Todos"] + ratings)

# Filtro por país principal
paises = sorted(df["main_country"].dropna().unique())
paises = [p for p in paises if p != "Sin información"]
selected_country = st.sidebar.selectbox("País", ["Todos"] + paises)

# Filtro por rango de años
min_year = int(df["release_year"].min())
max_year = int(df["release_year"].max())

year_range = st.sidebar.slider(
    "Rango de años de estreno",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)


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

st.subheader("Métricas descriptivas")

metricas = obtener_metricas(df_filtered)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total de títulos", metricas["total_titulos"])
col2.metric("Películas", metricas["total_peliculas"])
col3.metric("Series", metricas["total_series"])
col4.metric("Países distintos", metricas["total_paises"])
col5.metric("Géneros distintos", metricas["total_generos"])


# ── Tabla de datos filtrados ─────────────────────────────────────────────────

st.subheader("Tabla de datos filtrados")

st.dataframe(
    df_filtered[[
        "title",
        "type",
        "main_country",
        "release_year",
        "rating",
        "duration",
        "main_genre",
        "date_added",
    ]],
    use_container_width=True
)


# ── Visualizaciones ──────────────────────────────────────────────────────────

st.subheader("Visualizaciones")

col1, col2 = st.columns(2)

with col1:
    st.pyplot(plot_titles_by_type(df_filtered))

with col2:
    st.pyplot(plot_rating_distribution(df_filtered))

col3, col4 = st.columns(2)

with col3:
    st.pyplot(plot_top_genres(df_filtered))

with col4:
    st.pyplot(plot_top_countries(df_filtered))

st.pyplot(plot_titles_by_year(df_filtered))


# ── Top 10 títulos más recientes ─────────────────────────────────────────────

st.subheader("Top 10 títulos más recientes")

top_recientes = df_filtered.sort_values(by="release_year", ascending=False).head(10)

st.dataframe(
    top_recientes[[
        "title",
        "type",
        "release_year",
        "main_country",
        "rating",
        "main_genre",
        "duration",
    ]],
    use_container_width=True
)
