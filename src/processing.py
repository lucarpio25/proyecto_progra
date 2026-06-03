import pandas as pd


def limpiar_datos(df):
    """
    Limpia la base de datos de Netflix:
    - Elimina duplicados.
    - Completa valores faltantes en columnas categóricas.
    - Elimina registros sin título, tipo o año.
    """

    df = df.copy()

    df = df.drop_duplicates()

    df = df.dropna(subset=[
        "show_id",
        "type",
        "title",
        "release_year"
    ])

    columnas_texto = [
        "director",
        "cast",
        "country",
        "rating",
        "duration",
        "listed_in",
        "description"
    ]

    for columna in columnas_texto:
        df[columna] = df[columna].fillna("Sin información")
        df[columna] = df[columna].astype(str).str.strip()

    df["title"] = df["title"].astype(str).str.strip()
    df["type"] = df["type"].astype(str).str.strip()

    return df


def convertir_tipos_datos(df):
    """
    Convierte las columnas al tipo correcto:
    - date_added a fecha.
    - release_year a entero.
    """

    df = df.copy()

    df["date_added"] = pd.to_datetime(
        df["date_added"],
        errors="coerce"
    )

    df["release_year"] = pd.to_numeric(
        df["release_year"],
        errors="coerce"
    )

    df = df.dropna(subset=["release_year"])

    df["release_year"] = df["release_year"].astype(int)

    return df


def separar_duracion(df):
    """
    Separa la duración en número y unidad.
    Ejemplos:
    - 90 min -> duration_number = 90, duration_unit = min
    - 2 Seasons -> duration_number = 2, duration_unit = Seasons
    """

    df = df.copy()

    duracion = df["duration"].str.extract(r"(\d+)\s*(.*)")

    df["duration_number"] = pd.to_numeric(
        duracion[0],
        errors="coerce"
    )

    df["duration_unit"] = duracion[1].fillna("Sin información")

    return df


def crear_columnas_nuevas(df):
    """
    Crea columnas útiles para el análisis:
    - year_added
    - month_added
    - main_country
    - main_genre
    - content_age
    """

    df = df.copy()

    df["year_added"] = df["date_added"].dt.year
    df["month_added"] = df["date_added"].dt.month

    df["main_country"] = (
        df["country"]
        .str.split(",")
        .str[0]
        .str.strip()
    )

    df["main_genre"] = (
        df["listed_in"]
        .str.split(",")
        .str[0]
        .str.strip()
    )

    max_year = df["release_year"].max()
    df["content_age"] = max_year - df["release_year"]

    return df


def ordenar_datos(df):
    """
    Ordena los títulos por año de estreno, del más reciente al más antiguo.
    """

    df = df.copy()

    df = df.sort_values(
        by="release_year",
        ascending=False
    )

    return df


def seleccionar_columnas(df):
    """
    Selecciona las columnas que se usarán en la app.
    """

    df = df.copy()

    columnas = [
        "show_id",
        "type",
        "title",
        "director",
        "cast",
        "main_country",
        "country",
        "date_added",
        "year_added",
        "month_added",
        "release_year",
        "rating",
        "duration",
        "duration_number",
        "duration_unit",
        "listed_in",
        "main_genre",
        "content_age",
        "description"
    ]

    df = df[columnas]

    return df


def procesar_datos(df):
    """
    Ejecuta todo el procesamiento del dataset de Netflix.
    """

    df = limpiar_datos(df)
    df = convertir_tipos_datos(df)
    df = separar_duracion(df)
    df = crear_columnas_nuevas(df)
    df = ordenar_datos(df)
    df = seleccionar_columnas(df)

    return df


def obtener_metricas(df):
    """
    Calcula métricas descriptivas principales.
    """

    total_titulos = df.shape[0]
    total_peliculas = df[df["type"] == "Movie"].shape[0]
    total_series = df[df["type"] == "TV Show"].shape[0]
    total_paises = df["main_country"].nunique()
    total_generos = df["main_genre"].nunique()

    return {
        "total_titulos": total_titulos,
        "total_peliculas": total_peliculas,
        "total_series": total_series,
        "total_paises": total_paises,
        "total_generos": total_generos
    }


def obtener_generos_expandido(df):
    """
    Devuelve una serie con todos los géneros separados.
    Sirve para gráficos de top géneros.
    """

    generos = (
        df["listed_in"]
        .dropna()
        .str.split(", ")
        .explode()
    )

    return generos


def obtener_paises_expandido(df):
    """
    Devuelve una serie con todos los países separados.
    Sirve para gráficos de top países.
    """

    paises = (
        df["country"]
        .dropna()
        .str.split(", ")
        .explode()
    )

    paises = paises[paises != "Sin información"]

    return paises
