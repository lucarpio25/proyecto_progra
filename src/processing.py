import pandas as pd


def limpiar_datos(df):
    """
    Limpia la base de datos eliminando datos vacíos y duplicados.
    """

    df = df.copy()

    df = df.drop_duplicates()

    df = df.dropna(subset=[
        "Release_Date",
        "Title",
        "Popularity",
        "Vote_Count",
        "Vote_Average",
        "Original_Language",
        "Genre"
    ])

    return df


def convertir_tipos_datos(df):
    """
    Convierte las columnas a los tipos de datos correctos.
    """

    df = df.copy()

    df["Release_Date"] = pd.to_datetime(df["Release_Date"], errors="coerce")

    df["Popularity"] = pd.to_numeric(df["Popularity"], errors="coerce")
    df["Vote_Count"] = pd.to_numeric(df["Vote_Count"], errors="coerce")
    df["Vote_Average"] = pd.to_numeric(df["Vote_Average"], errors="coerce")

    df = df.dropna(subset=[
        "Release_Date",
        "Popularity",
        "Vote_Count",
        "Vote_Average"
    ])

    return df


def crear_columnas_nuevas(df):
    """
    Crea columnas nuevas útiles para el análisis.
    """

    df = df.copy()

    df["Year"] = df["Release_Date"].dt.year
    df["Month"] = df["Release_Date"].dt.month

    df["Vote_Category"] = df["Vote_Average"].apply(categorizar_voto)

    return df


def categorizar_voto(voto):
    """
    Clasifica las películas según su promedio de voto.
    """

    if voto >= 8:
        return "Muy buena"
    elif voto >= 6:
        return "Buena"
    elif voto >= 4:
        return "Regular"
    else:
        return "Baja"


def ordenar_datos(df):
    """
    Ordena las películas por popularidad.
    """

    df = df.copy()

    df = df.sort_values(by="Popularity", ascending=False)

    return df


def seleccionar_columnas(df):
    """
    Selecciona las columnas que se usarán en la aplicación.
    """

    df = df.copy()

    columnas = [
        "Title",
        "Overview",
        "Release_Date",
        "Year",
        "Month",
        "Popularity",
        "Vote_Count",
        "Vote_Average",
        "Vote_Category",
        "Original_Language",
        "Genre",
        "Poster_Url"
    ]

    df = df[columnas]

    return df


def procesar_datos(df):
    """
    Ejecuta todo el procesamiento de la base de datos.
    """

    df = limpiar_datos(df)
    df = convertir_tipos_datos(df)
    df = crear_columnas_nuevas(df)
    df = ordenar_datos(df)
    df = seleccionar_columnas(df)

    return df
