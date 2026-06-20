import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import numpy as np
from processing import obtener_generos_expandido, obtener_paises_expandido


# ── Paleta y tema Netflix ─────────────────────────────────────────────────────

BG_DARK   = "#0d0d0d"
BG_CARD   = "#141414"
BG_AXES   = "#111111"
RED       = "#E50914"
RED_LIGHT = "#ff3d46"
WHITE     = "#f0f0f0"
GRAY_1    = "#888888"
GRAY_2    = "#333333"
GRAY_3    = "#1e1e1e"

FONT_TITLE = {"fontfamily": "DejaVu Sans", "fontsize": 13,
              "fontweight": "bold", "color": WHITE, "pad": 14}
FONT_AXIS  = {"fontfamily": "DejaVu Sans", "fontsize": 9,
              "color": GRAY_1}

# Gradiente rojo para barras (de rojo oscuro a rojo vivo)
def _bar_colors(n):
    """Genera un array de colores en degradado de rojo oscuro → rojo vivo."""
    return [plt.cm.Reds(0.45 + 0.55 * i / max(n - 1, 1)) for i in range(n)]

def _base_fig(figsize=(10, 5)):
    """Crea figure y axes con el fondo y estilo base."""
    fig, ax = plt.subplots(figsize=figsize, facecolor=BG_DARK)
    ax.set_facecolor(BG_AXES)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRAY_2)
    ax.tick_params(colors=GRAY_1, labelsize=8.5, length=3)
    ax.xaxis.label.set_color(GRAY_1)
    ax.yaxis.label.set_color(GRAY_1)
    ax.yaxis.grid(True, color=GRAY_3, linewidth=0.7, linestyle="--", zorder=0)
    ax.set_axisbelow(True)
    ax.xaxis.grid(False)
    return fig, ax

def _set_labels(ax, title, xlabel, ylabel):
    ax.set_title(title, **FONT_TITLE)
    ax.set_xlabel(xlabel, **FONT_AXIS, labelpad=8)
    ax.set_ylabel(ylabel, **FONT_AXIS, labelpad=8)

def _add_value_labels(ax, bars, fmt="{:.0f}", color=WHITE, offset=4):
    """Añade etiquetas con el valor encima de cada barra."""
    for bar in bars:
        h = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            h + offset,
            fmt.format(h),
            ha="center", va="bottom",
            fontsize=7.5, color=color, fontweight="bold"
        )

def _red_accent_line(fig):
    """Dibuja una línea roja decorativa debajo del título."""
    fig.add_artist(
        plt.Line2D([0.08, 0.18], [0.91, 0.91],
                   transform=fig.transFigure,
                   color=RED, linewidth=2.5, solid_capstyle="round")
    )


# ── Gráficos ──────────────────────────────────────────────────────────────────

def plot_titles_by_type(df):
    """Cantidad de títulos por tipo (Movie / TV Show) — donut chart."""
    type_counts = df["type"].value_counts()

    fig, ax = plt.subplots(figsize=(8, 5), facecolor=BG_DARK)
    ax.set_facecolor(BG_DARK)

    colors  = [RED, "#333333"]
    explode = [0.04] * len(type_counts)

    wedges, texts, autotexts = ax.pie(
        type_counts,
        labels=None,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors,
        explode=explode,
        pctdistance=0.75,
        wedgeprops={"linewidth": 2.5, "edgecolor": BG_DARK},
    )
    for at in autotexts:
        at.set(color=WHITE, fontsize=11, fontweight="bold")

    # Agujero central (efecto donut)
    centre_circle = plt.Circle((0, 0), 0.52, fc=BG_DARK)
    ax.add_artist(centre_circle)

    # Texto central
    total = type_counts.sum()
    ax.text(0, 0.08, str(total),
            ha="center", va="center",
            fontsize=22, fontweight="bold", color=WHITE)
    ax.text(0, -0.18, "títulos",
            ha="center", va="center",
            fontsize=9, color=GRAY_1)

    # Leyenda
    legend_labels = [f"{k}  ({v:,})" for k, v in type_counts.items()]
    legend = ax.legend(
        wedges, legend_labels,
        loc="lower center", bbox_to_anchor=(0.5, -0.1),
        ncol=2, frameon=False,
        fontsize=10, labelcolor=GRAY_1
    )

    ax.set_title("Títulos por tipo de contenido", **FONT_TITLE)
    _red_accent_line(fig)
    ax.axis("equal")
    plt.tight_layout()
    return fig


def plot_top_genres(df):
    """Top 10 géneros — barras horizontales con degradado."""
    genres = obtener_generos_expandido(df)
    genre_counts = genres.value_counts().head(10).sort_values()

    fig, ax = plt.subplots(figsize=(10, 5.5), facecolor=BG_DARK)
    ax.set_facecolor(BG_AXES)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRAY_2)

    n = len(genre_counts)
    colors = _bar_colors(n)

    bars = ax.barh(
        genre_counts.index,
        genre_counts.values,
        color=colors,
        height=0.62,
        edgecolor="none",
        zorder=3,
    )

    # Etiquetas de valor al final de cada barra
    for bar, val in zip(bars, genre_counts.values):
        ax.text(
            val + genre_counts.max() * 0.01,
            bar.get_y() + bar.get_height() / 2,
            f"{val:,}",
            va="center", ha="left",
            fontsize=8, color=WHITE, fontweight="bold"
        )

    ax.tick_params(colors=GRAY_1, labelsize=8.5, length=0)
    ax.xaxis.grid(True, color=GRAY_3, linewidth=0.7, linestyle="--", zorder=0)
    ax.yaxis.grid(False)
    ax.set_axisbelow(True)
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_edgecolor(GRAY_2)

    _set_labels(ax, "Top 10 géneros más frecuentes", "Cantidad de títulos", "")
    ax.tick_params(axis="y", colors=WHITE, labelsize=9)
    ax.tick_params(axis="x", colors=GRAY_1, labelsize=8)
    _red_accent_line(fig)
    plt.tight_layout()
    return fig


def plot_titles_by_year(df):
    """Títulos por año de estreno — línea con área rellena."""
    titles_by_year = df.groupby("release_year").size().sort_index()

    fig, ax = plt.subplots(figsize=(12, 5), facecolor=BG_DARK)
    ax.set_facecolor(BG_AXES)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRAY_2)

    x = titles_by_year.index
    y = titles_by_year.values

    # Área con gradiente simulado
    ax.fill_between(x, y, alpha=0.18, color=RED, zorder=2)

    # Línea principal
    ax.plot(x, y, color=RED, linewidth=2.2, zorder=3)

    # Puntos en los extremos y máximo
    max_idx = y.argmax()
    highlight_x = [x[0], x[max_idx], x[-1]]
    highlight_y = [y[0], y[max_idx], y[-1]]
    ax.scatter(highlight_x, highlight_y,
               color=RED_LIGHT, s=60, zorder=5, edgecolors=BG_DARK, linewidths=1.5)

    # Etiqueta en el pico
    ax.annotate(
        f"  Pico: {y[max_idx]:,}",
        xy=(x[max_idx], y[max_idx]),
        fontsize=8.5, color=WHITE, fontweight="bold",
        va="bottom"
    )

    ax.yaxis.grid(True, color=GRAY_3, linewidth=0.7, linestyle="--", zorder=0)
    ax.xaxis.grid(False)
    ax.set_axisbelow(True)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)

    _set_labels(ax, "Títulos por año de estreno", "Año", "Cantidad de títulos")
    ax.tick_params(colors=GRAY_1, labelsize=8.5, length=3)
    _red_accent_line(fig)
    plt.tight_layout()
    return fig


def plot_top_countries(df):
    """Top 10 países — barras verticales con degradado y etiquetas."""
    countries = obtener_paises_expandido(df)
    country_counts = countries.value_counts().head(10)

    fig, ax = plt.subplots(figsize=(10, 5.5), facecolor=BG_DARK)
    ax.set_facecolor(BG_AXES)

    n = len(country_counts)
    colors = _bar_colors(n)[::-1]  # Más intenso en el primero

    bars = ax.bar(
        country_counts.index,
        country_counts.values,
        color=colors,
        width=0.62,
        edgecolor="none",
        zorder=3,
    )

    _add_value_labels(ax, bars, offset=country_counts.max() * 0.01)

    ax.tick_params(colors=GRAY_1, labelsize=8, length=3)
    ax.tick_params(axis="x", rotation=30)
    ax.yaxis.grid(True, color=GRAY_3, linewidth=0.7, linestyle="--", zorder=0)
    ax.xaxis.grid(False)
    ax.set_axisbelow(True)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["bottom", "left"]:
        ax.spines[spine].set_edgecolor(GRAY_2)

    _set_labels(ax, "Top 10 países con más contenido", "País", "Cantidad de títulos")
    ax.tick_params(axis="x", colors=WHITE)
    _red_accent_line(fig)
    plt.tight_layout()
    return fig


def plot_rating_distribution(df):
    """Distribución por clasificación — barras con el top resaltado."""
    rating_counts = df["rating"].value_counts().head(10).sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(10, 5), facecolor=BG_DARK)
    ax.set_facecolor(BG_AXES)

    n = len(rating_counts)
    # Primera barra en rojo vivo, el resto en tonos apagados
    colors = [RED if i == 0 else "#2e2e2e" for i in range(n)]

    bars = ax.bar(
        rating_counts.index,
        rating_counts.values,
        color=colors,
        width=0.6,
        edgecolor="none",
        zorder=3,
    )

    _add_value_labels(ax, bars, offset=rating_counts.max() * 0.01)

    ax.tick_params(colors=GRAY_1, labelsize=8.5, length=3)
    ax.tick_params(axis="x", rotation=0)
    ax.yaxis.grid(True, color=GRAY_3, linewidth=0.7, linestyle="--", zorder=0)
    ax.xaxis.grid(False)
    ax.set_axisbelow(True)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["bottom", "left"]:
        ax.spines[spine].set_edgecolor(GRAY_2)

    _set_labels(ax, "Distribución por clasificación", "Clasificación", "Cantidad de títulos")
    ax.tick_params(axis="x", colors=WHITE)

    # Badge "más común"
    ax.text(
        0, rating_counts.values[0] * 0.5,
        "más\ncomún", ha="center", va="center",
        fontsize=7, color=BG_DARK, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.2", fc=RED_LIGHT, ec="none")
    )

    _red_accent_line(fig)
    plt.tight_layout()
    return fig
