import matplotlib.pyplot as plt


def plot_top_genres(df):
    """
    Muestra los 10 géneros más frecuentes.
    Si una película tiene varios géneros separados por coma,
    los cuenta por separado.
    """

    df = df.copy()

    genres = df["Genre"].dropna().str.split(", ")
    genres = genres.explode()

    genre_counts = genres.value_counts().head(10)

    fig, ax = plt.subplots(figsize=(10, 5))

    genre_counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title("Top 10 géneros más frecuentes")
    ax.set_xlabel("Género")
    ax.set_ylabel("Cantidad de películas")

    ax.tick_params(axis="x", rotation=45)

    plt.tight_layout()

    return fig


def plot_movies_by_year(df):
    """
    Muestra la cantidad de películas estrenadas por año.
    """

    df = df.copy()

    movies_by_year = df.groupby("Year").size().sort_index()

    fig, ax = plt.subplots(figsize=(10, 5))

    movies_by_year.plot(
        kind="line",
        marker="o",
        ax=ax
    )

    ax.set_title("Cantidad de películas por año")
    ax.set_xlabel("Año")
    ax.set_ylabel("Cantidad de películas")

    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    return fig


def plot_vote_distribution(df):
    """
    Muestra la distribución de calificaciones promedio.
    """

    df = df.copy()

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.hist(
        df["Vote_Average"].dropna(),
        bins=20,
        edgecolor="black"
    )

    ax.set_title("Distribución de calificaciones")
    ax.set_xlabel("Calificación promedio")
    ax.set_ylabel("Cantidad de películas")

    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    return fig


def plot_top_popular_movies(df):
    """
    Muestra las 10 películas con mayor popularidad.
    """

    df = df.copy()

    top_movies = df.sort_values(
        by="Popularity",
        ascending=False
    ).head(10)

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.barh(
        top_movies["Title"],
        top_movies["Popularity"]
    )

    ax.set_title("Top 10 películas más populares")
    ax.set_xlabel("Popularidad")
    ax.set_ylabel("Película")

    ax.invert_yaxis()

    plt.tight_layout()

    return fig


def plot_vote_category(df):
    """
    Muestra la cantidad de películas por categoría de calificación.
    Usa la columna Vote_Category creada en processing.py.
    """

    df = df.copy()

    vote_counts = df["Vote_Category"].value_counts()

    fig, ax = plt.subplots(figsize=(8, 5))

    vote_counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title("Cantidad de películas por categoría de calificación")
    ax.set_xlabel("Categoría")
    ax.set_ylabel("Cantidad de películas")

    ax.tick_params(axis="x", rotation=0)

    plt.tight_layout()

    return fig


def plot_language_distribution(df):
    """
    Muestra los 10 idiomas originales más frecuentes.
    """

    df = df.copy()

    language_counts = df["Original_Language"].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(10, 5))

    language_counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title("Top 10 idiomas originales")
    ax.set_xlabel("Idioma")
    ax.set_ylabel("Cantidad de películas")

    ax.tick_params(axis="x", rotation=0)

    plt.tight_layout()

    return fig


def plot_popularity_vs_vote(df):
    """
    Muestra la relación entre popularidad y calificación promedio.
    """

    df = df.copy()

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.scatter(
        df["Vote_Average"],
        df["Popularity"],
        alpha=0.5
    )

    ax.set_title("Relación entre calificación y popularidad")
    ax.set_xlabel("Calificación promedio")
    ax.set_ylabel("Popularidad")

    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    return fig
