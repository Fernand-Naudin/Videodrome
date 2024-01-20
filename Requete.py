import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
from io import StringIO

# Chargement et préparation des données
# URL du fichier CSV sur GitHub
csv_url = 'https://raw.githubusercontent.com/Fernand-Naudin/Videodrome/main/final_merged_imdb_akas_2023-11-26_16h02m36s_m.csv'
print(csv_url)

# Envoyer une requête HTTP GET pour obtenir le contenu du fichier CSV
response = requests.get(csv_url)
print(response)
response.raise_for_status()  # Vérifier que la requête a réussi

# Convertir le contenu en texte en un objet fichier utilisable par Pandas
csv_raw = StringIO(response.text)

# Utiliser pandas pour lire le fichier CSV
df = pd.read_csv(csv_raw)

# Afficher les premières lignes du DataFrame pour vérifier
print(df.head())
