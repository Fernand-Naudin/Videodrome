import streamlit as st
import pandas as pd

@st.cache  # Utiliser le cache pour éviter de recharger les données à chaque interaction
def load_data(url):
    # Utiliser pandas pour lire le fichier CSV directement depuis l'URL
    df = pd.read_csv(url)
    return df

# URL du fichier CSV sur GitHub (s'assurer que c'est l'URL du fichier brut/raw)
csv_url = 'https://raw.githubusercontent.com/Fernand-Naudin/Videodrome/main/final_merged_imdb_akas_2023-11-26_16h02m36s_m.csv'

# Charger les données
df = load_data(csv_url)

# Afficher le DataFrame dans l'application
st.write("Aperçu des données :")
st.dataframe(df)



