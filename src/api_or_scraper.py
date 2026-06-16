import os
import time
from functools import wraps

import requests
from dotenv import load_dotenv


load_dotenv()


def medir_tiempo(func):
    """
    Decorador para medir el tiempo de ejecución de una función.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fin = time.time()

        print(f"{func.__name__} ejecutado en {fin - inicio:.2f} segundos")

        return resultado

    return wrapper


def obtener_api_key():
    """
    Obtiene la API key de OMDb desde el archivo .env.
    """

    api_key = os.getenv("OMDB_API_KEY")

    if not api_key:
        raise ValueError(
            "No se encontró OMDB_API_KEY. Revisa que exista el archivo .env."
        )

    return api_key


def convertir_tipo_netflix_a_omdb(tipo):
    """
    Convierte los tipos del dataset de Netflix al formato usado por OMDb.

    Netflix usa:
    - Movie
    - TV Show

    OMDb usa:
    - movie
    - series
    """

    if tipo == "Movie":
        return "movie"

    if tipo == "TV Show":
        return "series"

    return None


def limpiar_valor(valor):
    """
    Convierte valores 'N/A' o vacíos en None.
    """

    if valor in ["N/A", "", None]:
        return None

    return valor


@medir_tiempo
def buscar_titulo_omdb(titulo, tipo=None, anio=None):
    """
    Busca un título en OMDb usando título, tipo y año.

    Parámetros:
    - titulo: nombre de la película o serie.
    - tipo: Movie o TV Show.
    - anio: año de estreno.

    Retorna:
    - Diccionario con datos externos si encuentra resultado.
    - None si no encuentra resultado o si ocurre un error.
    """

    api_key = obtener_api_key()
    url = "https://www.omdbapi.com/"

    params = {
        "apikey": api_key,
        "t": titulo,
        "r": "json",
        "plot": "short"
    }

    tipo_omdb = convertir_tipo_netflix_a_omdb(tipo)

    if tipo_omdb:
        params["type"] = tipo_omdb

    if anio:
        params["y"] = int(anio)

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if data.get("Response") == "False":
            return None

        resultado = {
            "imdb_id": limpiar_valor(data.get("imdbID")),
            "title_omdb": limpiar_valor(data.get("Title")),
            "year_omdb": limpiar_valor(data.get("Year")),
            "rated_omdb": limpiar_valor(data.get("Rated")),
            "runtime_omdb": limpiar_valor(data.get("Runtime")),
            "genre_omdb": limpiar_valor(data.get("Genre")),
            "director_omdb": limpiar_valor(data.get("Director")),
            "actors_omdb": limpiar_valor(data.get("Actors")),
            "plot_omdb": limpiar_valor(data.get("Plot")),
            "language_omdb": limpiar_valor(data.get("Language")),
            "country_omdb": limpiar_valor(data.get("Country")),
            "awards_omdb": limpiar_valor(data.get("Awards")),
            "poster_omdb": limpiar_valor(data.get("Poster")),
            "imdb_rating": limpiar_valor(data.get("imdbRating")),
            "imdb_votes": limpiar_valor(data.get("imdbVotes")),
            "type_omdb": limpiar_valor(data.get("Type")),
            "source": "OMDb API"
        }

        return resultado

    except requests.exceptions.Timeout:
        print(f"Tiempo de espera agotado al buscar: {titulo}")
        return None

    except requests.exceptions.ConnectionError:
        print(f"Error de conexión al buscar: {titulo}")
        return None

    except requests.exceptions.HTTPError as e:
        print(f"Error HTTP al buscar {titulo}: {e}")
        return None

    except requests.exceptions.RequestException as e:
        print(f"Error general de request al buscar {titulo}: {e}")
        return None

    except ValueError as e:
        print(f"Error procesando la respuesta para {titulo}: {e}")
        return None


def enriquecer_dataframe_con_omdb(df, limite=50):
    """
    Enriquece una muestra del DataFrame de Netflix con datos externos de OMDb.

    Se usa un límite para no hacer demasiadas llamadas a la API.
    """

    df_muestra = df.head(limite).copy()
    resultados = []

    for _, row in df_muestra.iterrows():
        resultado = buscar_titulo_omdb(
            titulo=row["title"],
            tipo=row["type"],
            anio=row["release_year"]
        )

        if resultado:
            resultado["show_id"] = row["show_id"]
            resultado["netflix_title"] = row["title"]
            resultado["netflix_type"] = row["type"]
            resultado["netflix_release_year"] = row["release_year"]

            resultados.append(resultado)

    return resultados


def probar_api():
    """
    Prueba rápida para verificar que la API funciona.
    """

    resultado = buscar_titulo_omdb(
        titulo="Stranger Things",
        tipo="TV Show",
        anio=2016
    )

    return resultado


if __name__ == "__main__":
    print(probar_api())
