import pandas as pd

from api_or_scraper import enriquecer_dataframe_con_omdb
from db import (
    obtener_show_ids_enriquecidos,
    contar_registros,
    crear_tablas,
    guardar_external_ratings,
    guardar_genres,
    guardar_titles, 
    registrar_intentos_api,
)
from processing import procesar_datos


DATA_PATH = "data/netflix_titles.csv"


def main():
    """
    Construye la base SQLite desde el CSV y OMDb.
    """

    print("1. Leyendo el CSV de Netflix...")

    df_raw = pd.read_csv(
        DATA_PATH,
        engine="python",
        on_bad_lines="skip",
    )

    print(f"   Filas originales: {len(df_raw)}")

    print("2. Procesando datos...")

    df = procesar_datos(df_raw)

    print(f"   Filas procesadas: {len(df)}")

    print("3. Creando tablas SQLite...")

    crear_tablas()

    print("4. Guardando catálogo de Netflix...")

    guardar_titles(df)

    print("5. Guardando géneros separados...")

    guardar_genres(df)

    print("6. Consultando OMDb...")

    # Empieza con 5 para comprobar que funciona.
    # Luego puedes aumentar a 20, 50 o más.
    show_ids_enriquecidos = obtener_show_ids_enriquecidos()

    df_pendiente = df[
        ~df["show_id"].isin(show_ids_enriquecidos)
    ].copy()

    print(f"   Ya enriquecidos: {len(show_ids_enriquecidos)}")
    print(f"   Pendientes: {len(df_pendiente)}")

    resultados, intentos = enriquecer_dataframe_con_omdb(
        df_pendiente,
        limite=200,
    )

    print(f"   Resultados encontrados en OMDb: {len(resultados)}")

    print("7. Guardando datos externos...")

    guardados = guardar_external_ratings(resultados)
    intentos_guardados = registrar_intentos_api(intentos)

    print(f"   Registros externos guardados: {guardados}")
    print(f"   Intentos registrados: {intentos_guardados}")

    print("8. Conteo final de tablas:")

    conteos = contar_registros()

    for tabla, cantidad in conteos.items():
        print(f"   {tabla}: {cantidad}")

    print("Base de datos construida correctamente.")


if __name__ == "__main__":
    main()
