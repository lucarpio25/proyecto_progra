import matplotlib.pyplot as plt

from processing import obtener_generos_expandido, obtener_paises_expandido


def plot_titles_by_type(df):
    """
    Muestra la cantidad de títulos por tipo: Movie o TV Show.
    """

    type_counts = df["type"].value_counts()

    fig, ax = plt.subplots(figsize=(8, 5))

    type_counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title("Cantidad de títulos por tipo")
    ax.set_xlabel("Tipo de contenido")
    ax.set_ylabel("Cantidad")

    ax.tick_params(axis="x", rotation=0)

    plt.tight_layout()

    return fig


def plot_top_genres(df):
    """
    Muestra los 10 géneros más frecuentes.
    """

    genres = obtener_generos_expandido(df)
    genre_counts = genres.value_counts().head(10)

    fig, ax = plt.subplots(figsize=(10, 5))

    genre_counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title("Top 10 géneros más frecuentes")
    ax.set_xlabel("Género")
    ax.set_ylabel("Cantidad de títulos")

    ax.tick_params(axis="x", rotation=45)

    plt.tight_layout()

    return fig


def plot_titles_by_year(df):
    """
    Muestra la cantidad de títulos por año de estreno.
    """

    titles_by_year = df.groupby("release_year").size().sort_index()

    fig, ax = plt.subplots(figsize=(10, 5))

    titles_by_year.plot(
        kind="line",
        marker="o",
        ax=ax
    )

    ax.set_title("Cantidad de títulos por año de estreno")
    ax.set_xlabel("Año de estreno")
    ax.set_ylabel("Cantidad de títulos")

    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    return fig


def plot_top_countries(df):
    """
    Muestra los 10 países con más títulos en el catálogo.
    """

    countries = obtener_paises_expandido(df)
    country_counts = countries.value_counts().head(10)

    fig, ax = plt.subplots(figsize=(10, 5))

    country_counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title("Top 10 países con más contenido")
    ax.set_xlabel("País")
    ax.set_ylabel("Cantidad de títulos")

    ax.tick_params(axis="x", rotation=45)

    plt.tight_layout()

    return fig


def plot_rating_distribution(df):
    """
    Muestra la distribución de títulos por clasificación.
    """

    rating_counts = df["rating"].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(10, 5))

    rating_counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title("Distribución por clasificación")
    ax.set_xlabel("Clasificación")
    ax.set_ylabel("Cantidad de títulos")

    ax.tick_params(axis="x", rotation=0)

    plt.tight_layout()

    return fig
