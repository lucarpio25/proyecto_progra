# Dashboard del Catálogo de Netflix

## Descripción

Este proyecto corresponde a la entrega final del curso **Programación Avanzada para la Ciencia de Datos**.

La aplicación fue desarrollada utilizando **Streamlit** y permite analizar un dataset del catálogo de Netflix mediante filtros interactivos, métricas descriptivas, visualizaciones y consultas sobre datos enriquecidos obtenidos desde fuentes externas.

El proyecto integra procesamiento de datos con **Pandas**, persistencia mediante **SQLite** y consumo de datos externos a través de la **API de OMDb**, permitiendo complementar la información original del catálogo con calificaciones y métricas provenientes de IMDb.

---

## Integrantes

* Luciana Carpio
* Sofia Briceño
* Gustavo Barrantes
* Maria Paz Vecco

---

## Dataset

El archivo utilizado es `netflix_titles.csv`, que contiene información sobre 8,807 películas y series disponibles en Netflix.

**Fuente:**

Bansal, S. (2021). *Netflix Movies and TV Shows* [Dataset]. Kaggle.

https://www.kaggle.com/datasets/shivamb/netflix-shows

**Licencia:** CC0 1.0 Universal (Dominio Público).

### Variables principales

* `type`: tipo de contenido (película o serie).
* `title`: título.
* `director`: director.
* `cast`: elenco.
* `country`: país o países de producción.
* `date_added`: fecha en que el contenido fue agregado a Netflix.
* `release_year`: año de estreno.
* `rating`: clasificación del contenido.
* `duration`: duración en minutos o temporadas.
* `listed_in`: géneros o categorías.
* `description`: descripción del título.

---

## Procesamiento de datos

La limpieza y transformación de datos se realizó en `src/processing.py` e incluyó:

* Eliminación de registros duplicados.
* Tratamiento de valores faltantes.
* Conversión de tipos de datos.
* Conversión de fechas.
* Separación de duración en valor numérico y unidad.
* Creación de variables derivadas.
* Ordenamiento y selección de columnas finales.

### Variables generadas

* `year_added`
* `month_added`
* `main_country`
* `main_genre`
* `content_age`
* `duration_number`
* `duration_unit`

### Métricas descriptivas

* Total de títulos.
* Total de películas.
* Total de series.
* Total de países.
* Total de géneros.

---

## Integración con datos externos

Para enriquecer el catálogo original de Netflix se utilizó la API de OMDb.

A partir de cada título se obtuvieron datos adicionales como:

* IMDb Rating.
* Cantidad de votos en IMDb.
* Director.
* Sinopsis.
* Póster oficial.
* Año de lanzamiento validado.
* Tipo de contenido.

La búsqueda utiliza coincidencia inteligente basada en título, año y similitud textual para mejorar la calidad de los resultados obtenidos.

---

## Base de datos SQLite

La información procesada y enriquecida se almacena en una base de datos SQLite.

### Tablas principales

#### titles

Contiene el catálogo procesado de Netflix.

#### genres

Contiene los géneros normalizados para facilitar consultas y análisis.

#### external_ratings

Contiene la información obtenida desde OMDb e IMDb.

#### api_search_log

Registra las consultas realizadas a la API para fines de auditoría y control.

---

## Arquitectura del sistema

El flujo general del proyecto es:

CSV Netflix
→ Limpieza y transformación (Pandas)
→ Consulta a OMDb API
→ Persistencia en SQLite
→ Consultas SQL
→ Dashboard interactivo en Streamlit

### Componentes principales

* `processing.py`: limpieza y transformación de datos.
* `api_or_scraper.py`: integración con OMDb.
* `db.py`: gestión de SQLite.
* `build_database.py`: construcción y carga de la base de datos.
* `viz.py`: generación de visualizaciones.
* `app.py`: interfaz principal en Streamlit.

---

## Funcionalidades

### Análisis del catálogo Netflix

* Carga de archivos CSV.
* Limpieza y transformación automática.
* Métricas descriptivas.
* Tabla interactiva.
* Filtros por:

  * Tipo de contenido.
  * Clasificación.
  * País.
  * Género.
  * Año de estreno.

### Visualizaciones

* Títulos por tipo de contenido.
* Top géneros más frecuentes.
* Títulos por año de estreno.
* Top países con más contenido.
* Distribución por clasificación.

### Análisis enriquecido con IMDb

* Distribución de ratings IMDb.
* Top títulos mejor valorados según IMDb.
* Promedio IMDb por tipo de contenido.
* Cantidad de títulos enriquecidos por categoría.
* Tarjetas visuales con información detallada.
* Visualización de pósters obtenidos desde OMDb.

### Funcionalidades avanzadas

* Persistencia mediante SQLite.
* Enriquecimiento automático usando API externa.
* Consulta de títulos almacenados.
* Búsqueda en vivo en OMDb desde la aplicación.
* Registro de consultas realizadas a la API.

---

## Estructura del proyecto

```text
proyecto_progra/
├── README.md
├── requirements.txt
├── .env.example
├── data/
│   └── netflix_titles.csv
├── database/
│   └── netflix.db
├── docs/
├── src/
│   ├── app.py
│   ├── processing.py
│   ├── viz.py
│   ├── db.py
│   ├── api_or_scraper.py
│   └── build_database.py
└── tests/
```

## Instalación y ejecución local

### 1. Clonar el repositorio

```bash
git clone https://github.com/lucarpio25/proyecto_progra.git
cd proyecto_progra
```

### 2. Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar la API de OMDb

Regístrate para obtener una API Key gratuita:

https://www.omdbapi.com/apikey.aspx

Crea un archivo `.env` en la raíz del proyecto:

```env
OMDB_API_KEY=TU_API_KEY
```

También puedes utilizar el archivo `.env.example` como plantilla.

**Importante:** el archivo `.env` no debe subirse al repositorio.

### 5. Construir la base de datos

```bash
python3 src/build_database.py
```

Este proceso:

* Lee el CSV original.
* Procesa y limpia los datos.
* Consulta la API de OMDb.
* Almacena los resultados en SQLite.

### 6. Ejecutar la aplicación

```bash
streamlit run src/app.py
```

Luego abre:

http://localhost:8501

---

## Tecnologías utilizadas

* Python
* Pandas
* Streamlit
* SQLite
* Requests
* Matplotlib
* OMDb API
* Git y GitHub

---

## Referencias

### Referencia de dashboard

Rahmad, A. (2023). *Netflix Data Analysis with Streamlit* [Repositorio GitHub].

https://github.com/ahmadrahmadx/Netflix-Data-Analysis

Sirvió como referencia para la organización del dashboard y la presentación de filtros interactivos.

### Documentación oficial

Streamlit. (2024). *Streamlit Documentation*.

https://docs.streamlit.io

Utilizada para implementar controles interactivos, métricas y visualizaciones.

### Fuente de datos externos

OMDb API.

https://www.omdbapi.com

Utilizada para enriquecer el catálogo con información adicional proveniente de IMDb.
