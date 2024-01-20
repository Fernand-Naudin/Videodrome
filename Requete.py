import streamlit as st
import pandas as pd

# Widget pour téléverser un fichier
uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="csv")

if uploaded_file is not None:
    # Lire le fichier CSV
    df = pd.read_csv(uploaded_file)
    
    # Afficher le DataFrame dans l'application
    st.write("Aperçu des données :")
    st.write(df.head())  # Affiche les premières lignes du DataFrame



