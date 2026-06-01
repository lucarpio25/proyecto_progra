import streamlit as st
import pandas as pd
from processing import procesar_datos

st.title("Análisis de películas")

df = pd.read_csv("data/mymoviedb.csv", engine="python", on_bad_lines="skip")
df = procesar_datos(df)

st.dataframe(df)






