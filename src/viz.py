import matplotlib.pyplot as plt


def plot_top_genres(df):
    """
    Top 10 géneros más frecuentes.
    """

    genre_counts = df["Genre"].value_counts().head(10)

    fig, ax = plt.subplots()

    genre_counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title("Top 10 géneros más frecuentes")
    ax.set_xlabel("Género")
    ax.set_ylabel("Cantidad de películas")

    plt.xticks(rotation=45)

    return fig


def plot_movies_by_year(df):
    """
    Cantidad de películas por año.
    """

    movies_by_year = df.groupby("Year").size()

    fig, ax = plt.subplots()

    movies_by_year.plot(
        kind="line",
        marker="o",
        ax=ax
    )

    ax.set_title("Películas por año")
    ax.set_xlabel("Año")
    ax.set_ylabel("Cantidad")

    return fig


def plot_vote_distribution(df):
    """
    Histograma de calificaciones.
    """

    fig, ax = plt.subplots()

    ax.hist(
        df["Vote_Average"],
        bins=20
    )

    ax.set_title("Distribución de calificaciones")
    ax.set_xlabel("Calificación")
    ax.set_ylabel("Frecuencia")

    return fig
