import sqlite3
from pathlib import Path

import pandas as pd


# Ruta absoluta basada en la ubicación del proyecto.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "database" / "netflix.db"

def obtener_show_ids_enriquecidos():
    """
    Devuelve los show_id que ya tienen información de OMDb.
    """

    query = """
        SELECT show_id
        FROM external_ratings
    """

    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query)

        return {
            fila[0]
            for fila in cursor.fetchall()
        }

def conectar_db(db_path=DB_PATH):
    """
    Crea y devuelve una conexión a SQLite.

    También activa las restricciones de claves foráneas.
    """

    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")

    return conn

def registrar_intento_api(show_id, status, message=None):
    """
    Registra si un título fue encontrado o no en OMDb.
    """

    query = """
        INSERT INTO api_search_log (
            show_id,
            status,
            message
        )
        VALUES (?, ?, ?)

        ON CONFLICT(show_id) DO UPDATE SET
            status = excluded.status,
            message = excluded.message,
            attempted_at = CURRENT_TIMESTAMP
    """

    with conectar_db() as conn:
        conn.execute(
            query,
            (show_id, status, message),
        )
        conn.commit()

def registrar_intentos_api(intentos):
    """
    Registra varios intentos de búsqueda en api_search_log.
    """

    if not intentos:
        return 0

    query = """
        INSERT INTO api_search_log (
            show_id,
            status,
            message
        )
        VALUES (?, ?, ?)

        ON CONFLICT(show_id) DO UPDATE SET
            status = excluded.status,
            message = excluded.message,
            attempted_at = CURRENT_TIMESTAMP
    """

    filas = [
        (
            intento.get("show_id"),
            intento.get("status"),
            intento.get("message"),
        )
        for intento in intentos
    ]

    with conectar_db() as conn:
        conn.executemany(query, filas)
        conn.commit()

    return len(filas)


def obtener_show_ids_procesados():
    """
    Devuelve los títulos ya intentados, encontrados o no.
    """

    query = """
        SELECT show_id
        FROM api_search_log
    """

    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query)

        return {
            fila[0]
            for fila in cursor.fetchall()
        }


def crear_tablas():
    """
    Crea las tablas del proyecto si todavía no existen.

    Tablas:
    - titles: catálogo procesado de Netflix.
    - external_ratings: información obtenida desde OMDb.
    - genres: géneros separados de cada título.
    """

    with conectar_db() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS titles (
                show_id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                title TEXT NOT NULL,
                director TEXT,
                cast_members TEXT,
                main_country TEXT,
                country TEXT,
                date_added TEXT,
                year_added INTEGER,
                month_added INTEGER,
                release_year INTEGER NOT NULL,
                rating TEXT,
                duration TEXT,
                duration_number REAL,
                duration_unit TEXT,
                listed_in TEXT,
                main_genre TEXT,
                content_age INTEGER,
                description TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS external_ratings (
                show_id TEXT PRIMARY KEY,
                imdb_id TEXT,
                title_omdb TEXT,
                year_omdb TEXT,
                rated_omdb TEXT,
                runtime_omdb TEXT,
                genre_omdb TEXT,
                director_omdb TEXT,
                actors_omdb TEXT,
                plot_omdb TEXT,
                language_omdb TEXT,
                country_omdb TEXT,
                awards_omdb TEXT,
                poster_omdb TEXT,
                imdb_rating REAL,
                imdb_votes INTEGER,
                type_omdb TEXT,
                source TEXT,
		match_method TEXT,
		similarity_score REAL,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (show_id)
                    REFERENCES titles(show_id)
                    ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS genres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                show_id TEXT NOT NULL,
                genre TEXT NOT NULL,
                FOREIGN KEY (show_id)
                    REFERENCES titles(show_id)
                    ON DELETE CASCADE,
                UNIQUE (show_id, genre)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS api_search_log (
                show_id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                attempted_at TEXT DEFAULT CURRENT_TIMESTAMP,
                message TEXT,
                FOREIGN KEY (show_id)
                    REFERENCES titles(show_id)
                    ON DELETE CASCADE
            )
        """)
        conn.commit()


def convertir_valor_sql(valor):
    """
    Convierte valores de pandas que SQLite no maneja bien.

    NaN o NaT se transforman en None.
    """

    if pd.isna(valor):
        return None

    if isinstance(valor, pd.Timestamp):
        return valor.isoformat()

    return valor


def guardar_titles(df):
    """
    Guarda o actualiza el catálogo procesado de Netflix.

    Usa INSERT OR REPLACE para conservar el esquema SQL,
    la clave primaria y las relaciones.
    """

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
        "description",
    ]

    df_titles = df[columnas].copy()

    # La palabra cast puede causar confusión en SQL,
    # por eso se guarda como cast_members.
    df_titles = df_titles.rename(
        columns={"cast": "cast_members"}
    )

    filas = []

    for row in df_titles.itertuples(index=False, name=None):
        filas.append(
            tuple(convertir_valor_sql(valor) for valor in row)
        )
    query = """
        INSERT INTO titles (
            show_id,
            type,
            title,
            director,
            cast_members,
            main_country,
            country,
            date_added,
            year_added,
            month_added,
            release_year,
            rating,
            duration,
            duration_number,
            duration_unit,
            listed_in,
            main_genre,
            content_age,
            description
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        ON CONFLICT(show_id) DO UPDATE SET
            type = excluded.type,
            title = excluded.title,
            director = excluded.director,
            cast_members = excluded.cast_members,
            main_country = excluded.main_country,
            country = excluded.country,
            date_added = excluded.date_added,
            year_added = excluded.year_added,
            month_added = excluded.month_added,
            release_year = excluded.release_year,
            rating = excluded.rating,
            duration = excluded.duration,
            duration_number = excluded.duration_number,
            duration_unit = excluded.duration_unit,
            listed_in = excluded.listed_in,
            main_genre = excluded.main_genre,
            content_age = excluded.content_age,
            description = excluded.description
    """

    with conectar_db() as conn:
        conn.executemany(query, filas)
        conn.commit()


def guardar_genres(df):
    """
    Separa los géneros de listed_in y los guarda
    en una tabla relacionada.
    """

    filas = []

    for _, row in df.iterrows():
        show_id = row["show_id"]
        listed_in = row["listed_in"]

        if pd.isna(listed_in):
            continue

        generos = str(listed_in).split(", ")

        for genero in generos:
            genero = genero.strip()

            if genero:
                filas.append((show_id, genero))

    query = """
        INSERT OR IGNORE INTO genres (
            show_id,
            genre
        )
        VALUES (?, ?)
    """

    with conectar_db() as conn:
        conn.executemany(query, filas)
        conn.commit()


def limpiar_imdb_rating(valor):
    """
    Convierte el rating de IMDb a float.
    """

    if valor in [None, "", "N/A"]:
        return None

    try:
        return float(valor)
    except (TypeError, ValueError):
        return None


def limpiar_imdb_votes(valor):
    """
    Convierte votos como '1,234,567' a entero.
    """

    if valor in [None, "", "N/A"]:
        return None

    try:
        return int(str(valor).replace(",", ""))
    except (TypeError, ValueError):
        return None


def guardar_external_ratings(resultados):
    """
    Guarda o actualiza los resultados obtenidos desde OMDb.

    resultados debe ser una lista de diccionarios generada por:
    enriquecer_dataframe_con_omdb()
    """

    if not resultados:
        return 0

    query = """
        INSERT INTO external_ratings (
            show_id,
            imdb_id,
            title_omdb,
            year_omdb,
            rated_omdb,
            runtime_omdb,
            genre_omdb,
            director_omdb,
            actors_omdb,
            plot_omdb,
            language_omdb,
            country_omdb,
            awards_omdb,
            poster_omdb,
            imdb_rating,
            imdb_votes,
            type_omdb,
            source, 
	    match_method,
	    similarity_score
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        ON CONFLICT(show_id) DO UPDATE SET
            imdb_id = excluded.imdb_id,
            title_omdb = excluded.title_omdb,
            year_omdb = excluded.year_omdb,
            rated_omdb = excluded.rated_omdb,
            runtime_omdb = excluded.runtime_omdb,
            genre_omdb = excluded.genre_omdb,
            director_omdb = excluded.director_omdb,
            actors_omdb = excluded.actors_omdb,
            plot_omdb = excluded.plot_omdb,
            language_omdb = excluded.language_omdb,
            country_omdb = excluded.country_omdb,
            awards_omdb = excluded.awards_omdb,
            poster_omdb = excluded.poster_omdb,
            imdb_rating = excluded.imdb_rating,
            imdb_votes = excluded.imdb_votes,
            type_omdb = excluded.type_omdb,
            source = excluded.source, 
	    match_method = excluded.match_method,
	    similarity_score = excluded.similarity_score,
            updated_at = CURRENT_TIMESTAMP
    """

    filas = []

    for resultado in resultados:
        filas.append((
            resultado.get("show_id"),
            resultado.get("imdb_id"),
            resultado.get("title_omdb"),
            resultado.get("year_omdb"),
            resultado.get("rated_omdb"),
            resultado.get("runtime_omdb"),
            resultado.get("genre_omdb"),
            resultado.get("director_omdb"),
            resultado.get("actors_omdb"),
            resultado.get("plot_omdb"),
            resultado.get("language_omdb"),
            resultado.get("country_omdb"),
            resultado.get("awards_omdb"),
            resultado.get("poster_omdb"),
            limpiar_imdb_rating(resultado.get("imdb_rating")),
            limpiar_imdb_votes(resultado.get("imdb_votes")),
            resultado.get("type_omdb"),
            resultado.get("source"),
	    resultado.get("match_method"),
            resultado.get("similarity_score"),
        ))

    with conectar_db() as conn:
        conn.executemany(query, filas)
        conn.commit()

    return len(filas)


def consultar_catalogo():
    """
    Devuelve el catálogo completo almacenado en SQLite.
    """

    query = """
        SELECT *
        FROM titles
        ORDER BY release_year DESC, title ASC
    """

    with conectar_db() as conn:
        return pd.read_sql_query(query, conn)


def consultar_catalogo_enriquecido():
    """
    Une los datos de Netflix con los datos de OMDb.
    """

    query = """
        SELECT
            t.show_id,
            t.title,
            t.type,
            t.main_country,
            t.release_year,
            t.rating AS netflix_rating,
            t.duration,
            t.main_genre,
            t.description AS netflix_description,
            e.imdb_id,
            e.imdb_rating,
            e.imdb_votes,
            e.runtime_omdb,
            e.genre_omdb,
            e.director_omdb,
            e.actors_omdb,
            e.plot_omdb,
            e.awards_omdb,
            e.poster_omdb,
            e.source,
            e.updated_at
        FROM titles AS t
        LEFT JOIN external_ratings AS e
            ON t.show_id = e.show_id
        ORDER BY t.release_year DESC, t.title ASC
    """

    with conectar_db() as conn:
        return pd.read_sql_query(query, conn)


def consultar_top_imdb(limite=10, minimo_votos=1000):
    """
    Devuelve los títulos mejor calificados en IMDb.

    minimo_votos evita que títulos con muy pocos votos
    aparezcan injustamente en los primeros lugares.
    """

    query = """
        SELECT
            t.title,
            t.type,
            t.release_year,
            t.main_genre,
            e.imdb_rating,
            e.imdb_votes,
            e.poster_omdb
        FROM titles AS t
        INNER JOIN external_ratings AS e
            ON t.show_id = e.show_id
        WHERE
            e.imdb_rating IS NOT NULL
            AND e.imdb_votes >= ?
        ORDER BY
            e.imdb_rating DESC,
            e.imdb_votes DESC
        LIMIT ?
    """

    with conectar_db() as conn:
        return pd.read_sql_query(
            query,
            conn,
            params=(minimo_votos, limite),
        )


def obtener_metricas_db():
    """
    Calcula métricas directamente desde SQLite.
    """

    query = """
        SELECT
            COUNT(*) AS total_titles,
            SUM(CASE WHEN type = 'Movie' THEN 1 ELSE 0 END) AS total_movies,
            SUM(CASE WHEN type = 'TV Show' THEN 1 ELSE 0 END) AS total_series,
            COUNT(DISTINCT main_country) AS total_countries,
            COUNT(DISTINCT main_genre) AS total_main_genres
        FROM titles
    """

    with conectar_db() as conn:
        return pd.read_sql_query(query, conn).iloc[0].to_dict()


def obtener_metricas_omdb():
    """
    Calcula métricas de los datos externos guardados.
    """

    query = """
        SELECT
            COUNT(*) AS enriched_titles,
            ROUND(AVG(imdb_rating), 2) AS average_imdb_rating,
            MAX(imdb_rating) AS maximum_imdb_rating,
            SUM(imdb_votes) AS total_imdb_votes
        FROM external_ratings
    """

    with conectar_db() as conn:
        return pd.read_sql_query(query, conn).iloc[0].to_dict()


def contar_registros():
    """
    Cuenta registros de cada tabla para comprobar la carga.
    """

    with conectar_db() as conn:
        cursor = conn.cursor()

        resultado = {}

        for tabla in ["titles", "genres", "external_ratings"]:
            cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
            resultado[tabla] = cursor.fetchone()[0]

        return resultado
