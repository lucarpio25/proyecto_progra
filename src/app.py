import streamlit as st

from processing import load_data, clean_data, get_metrics


st.set_page_config(page_title="Dashboard de Películas", layout="wide")

st.title("Dashboard de Películas - Entrega Parcial")

st.write("App inicial del proyecto.")

DATA_PATH = "data/mymoviedb.csv"

df_raw = load_data(DATA_PATH)
