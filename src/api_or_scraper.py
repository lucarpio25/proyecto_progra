from db import registrar_intento_api
import os
import time
from functools import wraps
import re
import unicodedata
from difflib import SequenceMatcher

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

def normalizar_titulo(titulo):
    """
    Normaliza un título para facilitar comparaciones.

    Ejemplo:
    'Pokémon: Mewtwo Strikes Back'
    se convierte en:
    'pokemon mewtwo strikes back'
    """

    if titulo is None:
        return ""

    titulo = str(titulo).lower().strip()

    titulo = unicodedata.normalize("NFD", titulo)
    titulo = "".join(
        caracter
        for caracter in titulo
        if unicodedata.category(caracter) != "Mn"
    )

    titulo = re.sub(r"[^a-z0-9\s]", " ", titulo)
    titulo = re.sub(r"\s+", " ", titulo).strip()

    return titulo

def calcular_similitud(titulo_original, titulo_candidato):
    """
    Calcula la similitud entre dos títulos.

    Devuelve un valor entre 0 y 1.
    Cuanto más cerca de 1, más parecidos son.
    """

    titulo_original = normalizar_titulo(titulo_original)
    titulo_candidato = normalizar_titulo(titulo_candidato)

    return SequenceMatcher(
        None,
        titulo_original,
        titulo_candidato,
    ).ratio()

def hacer_request_omdb(params):
    """
    Ejecuta una solicitud a OMDb y devuelve el JSON.

    Maneja errores de conexión, timeout y API.
    """

    api_key = obtener_api_key()
    url = "https://www.omdbapi.com/"

    params = params.copy()
    params["apikey"] = api_key
    params["r"] = "json"

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10,
        )

        if response.status_code == 401:
            print(
                "API key inválida o no autorizada. "
                "Revisa el archivo .env."
            )
            return None

        response.raise_for_status()

        data = response.json()

        if data.get("Response") == "False":
            return None

        return data

    except requests.exceptions.Timeout:
        print("Tiempo de espera agotado al consultar OMDb.")
        return None

    except requests.exceptions.ConnectionError:
        print("Error de conexión con OMDb.")
        return None

    except requests.exceptions.HTTPError as error:
        print(f"Error HTTP consultando OMDb: {error}")
        return None

    except requests.exceptions.RequestException as error:
        print(f"Error general consultando OMDb: {error}")
        return None

    except ValueError as error:
        print(f"Respuesta JSON inválida: {error}")
        return None

def formatear_resultado_omdb(data):
    """
    Convierte la respuesta de OMDb al formato usado por el proyecto.
    """

    if not data:
        return None

    return {
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
        "source": "OMDb API",
    }


@medir_tiempo
def buscar_titulo_omdb(titulo, tipo=None, anio=None):
    """
    Busca un título directamente en OMDb.

    Primer intento:
    - título
    - tipo
    - año
    """

    params = {
        "t": titulo,
        "plot": "short",
    }

    tipo_omdb = convertir_tipo_netflix_a_omdb(tipo)

    if tipo_omdb:
        params["type"] = tipo_omdb

    if anio:
        params["y"] = int(anio)

    data = hacer_request_omdb(params)

    return formatear_resultado_omdb(data)


def buscar_candidatos_omdb(titulo, tipo=None):
    """
    Busca varios candidatos usando la búsqueda general de OMDb.
    """

    params = {
        "s": titulo,
    }

    tipo_omdb = convertir_tipo_netflix_a_omdb(tipo)

    if tipo_omdb:
        params["type"] = tipo_omdb

    data = hacer_request_omdb(params)

    if not data:
        return []

    return data.get("Search", [])


def seleccionar_mejor_candidato(
    titulo,
    candidatos,
    anio=None,
    similitud_minima=0.65,
):
    """
    Selecciona el candidato más parecido.

    Combina:
    - similitud del título;
    - coincidencia del año.
    """

    mejor_candidato = None
    mejor_puntaje = 0

    for candidato in candidatos:
        titulo_candidato = candidato.get("Title", "")
        anio_candidato = candidato.get("Year", "")

        similitud = calcular_similitud(
            titulo,
            titulo_candidato,
        )

        puntaje = similitud

        if anio:
            primer_anio = str(anio_candidato)[:4]

            if primer_anio == str(int(anio)):
                puntaje += 0.20

        if puntaje > mejor_puntaje:
            mejor_puntaje = puntaje
            mejor_candidato = candidato

    if mejor_candidato is None:
        return None

    similitud_titulo = calcular_similitud(
        titulo,
        mejor_candidato.get("Title", ""),
    )

    if similitud_titulo < similitud_minima:
        return None

    return mejor_candidato


def buscar_por_imdb_id(imdb_id):
    """
    Consulta todos los detalles de un título usando su IMDb ID.
    """

    if not imdb_id:
        return None

    params = {
        "i": imdb_id,
        "plot": "short",
    }

    data = hacer_request_omdb(params)

    return formatear_resultado_omdb(data)


@medir_tiempo
def buscar_titulo_omdb_inteligente(titulo, tipo=None, anio=None):
    """
    Busca un título utilizando varios intentos.

    1. Búsqueda exacta con año.
    2. Búsqueda exacta sin año.
    3. Búsqueda general y selección por similitud.
    4. Consulta final mediante IMDb ID.
    """

    # Intento 1: búsqueda exacta con año
    resultado = buscar_titulo_omdb(
        titulo=titulo,
        tipo=tipo,
        anio=anio,
    )

    if resultado:
        resultado["match_method"] = "exact_title_type_year"
        resultado["similarity_score"] = 1.0
        return resultado

    # Intento 2: búsqueda exacta sin año
    resultado = buscar_titulo_omdb(
        titulo=titulo,
        tipo=tipo,
        anio=None,
    )

    if resultado:
        similitud = calcular_similitud(
            titulo,
            resultado.get("title_omdb"),
        )

        if similitud >= 0.75:
            resultado["match_method"] = "exact_title_type"
            resultado["similarity_score"] = round(similitud, 3)
            return resultado

    # Intento 3: búsqueda general
    candidatos = buscar_candidatos_omdb(
        titulo=titulo,
        tipo=tipo,
    )

    mejor_candidato = seleccionar_mejor_candidato(
        titulo=titulo,
        candidatos=candidatos,
        anio=anio,
        similitud_minima=0.65,
    )

    if not mejor_candidato:
        return None

    imdb_id = mejor_candidato.get("imdbID")

    # Intento 4: obtener detalles mediante IMDb ID
    resultado = buscar_por_imdb_id(imdb_id)

    if not resultado:
        return None

    similitud = calcular_similitud(
        titulo,
        resultado.get("title_omdb"),
    )

    resultado["match_method"] = "fuzzy_search"
    resultado["similarity_score"] = round(similitud, 3)

    return resultado


def enriquecer_dataframe_con_omdb(df, limite=50):
    """
    Enriquece títulos de Netflix con OMDb.

    Devuelve:
    - resultados encontrados;
    - intentos realizados con su estado.
    """

    df_muestra = df.head(limite).copy()

    resultados = []
    intentos = []

    for _, row in df_muestra.iterrows():
        print(
            f"Buscando: {row['title']} "
            f"({row['release_year']})"
        )

        resultado = buscar_titulo_omdb_inteligente(
            titulo=row["title"],
            tipo=row["type"],
            anio=row["release_year"],
        )

        if resultado:
            resultado["show_id"] = row["show_id"]
            resultado["netflix_title"] = row["title"]
            resultado["netflix_type"] = row["type"]
            resultado["netflix_release_year"] = row["release_year"]

            resultados.append(resultado)

            intentos.append({
                "show_id": row["show_id"],
                "status": "found",
                "message": (
                    f"Encontrado como {resultado.get('title_omdb')}"
                ),
            })

            print(
                f"  Encontrado: {resultado.get('title_omdb')} "
                f"| método: {resultado.get('match_method')} "
                f"| similitud: {resultado.get('similarity_score')}"
            )

        else:
            intentos.append({
                "show_id": row["show_id"],
                "status": "not_found",
                "message": "No se encontró una coincidencia en OMDb",
            })

            print("  No encontrado")

    return resultados, intentos


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
