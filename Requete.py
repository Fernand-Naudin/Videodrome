import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
from io import StringIO

import requests

# URL du fichier CSV sur GitHub
csv_url = 'https://raw.githubusercontent.com/Fernand-Naudin/Videodrome/main/final_merged_imdb_akas_2023-11-26_16h02m36s_m.csv'

# Envoyer une requête GET
response = requests.get(csv_url)

# Vérifier que la requête a réussi
response.raise_for_status()

# Lire le contenu du fichier
content = response.text

# Afficher le contenu du fichier (ou une partie)
print(content[:500])  # Afficher les 500 premiers caractères

