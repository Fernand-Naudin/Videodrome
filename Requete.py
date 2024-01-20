# import streamlit as st
# import pandas as pd

# @st.cache  # Utiliser le cache pour éviter de recharger les données à chaque interaction
# def load_data(url):
#     # Utiliser pandas pour lire le fichier CSV directement depuis l'URL
#     df = pd.read_csv(url)
#     return df

# # URL du fichier CSV sur GitHub (s'assurer que c'est l'URL du fichier brut/raw)
# csv_url = 'https://raw.githubusercontent.com/Fernand-Naudin/Videodrome/main/final_merged_imdb_akas_2023-11-26_16h02m36s_m.csv'

# # Charger les données
# df = load_data(csv_url)

# # Afficher le DataFrame dans l'application
# st.write("Aperçu des données :")
# st.dataframe(df)


import pandas as pd
import requests
from io import StringIO

# URL du fichier CSV sur GitHub
csv_url = 'https://raw.githubusercontent.com/Fernand-Naudin/Videodrome/main/final_merged_imdb_akas_2023-11-26_16h02m36s_m.csv'

# Envoyer une requête HTTP GET pour obtenir le contenu du fichier CSV
response = requests.get(csv_url)
response.raise_for_status()  # Vérifier que la requête a réussi

# Convertir le contenu en texte en un objet fichier utilisable par Pandas
csv_raw = StringIO(response.text)

# Utiliser pandas pour lire le fichier CSV
df = pd.read_csv(csv_raw)

# Afficher les premières lignes du DataFrame pour vérifier
print(df.head())
