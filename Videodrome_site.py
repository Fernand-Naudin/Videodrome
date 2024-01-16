import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Configuration de la page pour utiliser toute la largeur
st.set_page_config(layout="wide")

# Chargement et préparation des données
@st.cache_data
def load_and_prepare_data():
    # Chemin vers le fichier CSV (à remplacer par votre chemin de fichier)
    data_path = "final_merged_imdb_akas_2023-11-26_16h02m36s.csv"
    # uploaded_file = st.file_uploader("https://github.com/Fernand-Naudin/Videodrome/tree/main/final_merged_imdb_akas_2023-11-26_16h02m36s.csv")
    
    # Chargement des données
    df = pd.read_csv(data_path, sep=",", low_memory=False)

    # Utilisation de la colonne 'genres' pour la similarité
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(df['genres'])

    # Calcul de la matrice de similarité cosinus
    cosine_sim = cosine_similarity(tfidf_matrix)

    return df, cosine_sim

# Fonction pour afficher les détails d'un film
def display_movie_details(movie_record):
    movie_title = movie_record['title'].upper()
    movie_year = movie_record['startYear']
    movie_genre = movie_record['genres']
    movie_runtime = movie_record['runtime']
    directors = movie_record['director']
    actors = movie_record['actor']
    actresses = movie_record['actress']
    movie_synopsis = movie_record['overview']

    base_url = "https://image.tmdb.org/t/p/w500"
    if pd.notna(movie_record['poster_path']):
        poster_path = movie_record['poster_path']
        full_poster_url = base_url + poster_path
        col1, col2 = st.columns([2, 3])
        with col1:
            st.image(full_poster_url, width=300)  # Affichage de l'image
        with col2:
            st.markdown(f"<h2 style='font-weight: bold;'>{movie_title} ({movie_year})</h2>", unsafe_allow_html=True)
            st.write(f"**Durée :** {movie_runtime} minutes")
            st.write(f"**Genre(s) :** {movie_genre}")
            st.write(f"**Réalisateur(s) :** {directors}")
            st.write(f"**Acteur(s) et Actrice(s) :** {actors}, {actresses}")
            st.markdown("<h4 style='font-weight: bold;'>Synopsis :</h4>", unsafe_allow_html=True)
            st.write(movie_synopsis)
    else:
        st.write("Aucune image disponible pour ce film.")

# Fonction pour recommander des films
def recommend_movies(selected_movie_id, df, cosine_sim_matrix, number_of_movies=10):
    if selected_movie_id not in df.index:
        return pd.DataFrame()  # Retourner un DataFrame vide si l'ID n'est pas trouvé

    # Année de sortie du film sélectionné
    selected_movie_year = df.loc[selected_movie_id, 'startYear']

    # Scores de similarité
    sim_scores = cosine_sim_matrix[selected_movie_id]
    sim_scores = sorted(list(enumerate(sim_scores)), key=lambda x: x[1], reverse=True)

    # Collecter les indices des films les plus similaires, en excluant le film sélectionné
    similar_movies_indices = [i[0] for i in sim_scores if i[0] != selected_movie_id]

    # Filtrer les films pour éviter les doublons et s'assurer qu'ils sont dans la plage de 5 ans
    recommended_movies_ids = set()
    filtered_movies = []
    for idx in similar_movies_indices:
        if len(filtered_movies) >= number_of_movies:
            break

        movie_year = df.loc[idx, 'startYear']
        movie_tconst = df.loc[idx, 'tconst']
        if abs(selected_movie_year - movie_year) <= 5 and movie_tconst not in recommended_movies_ids:
            filtered_movies.append(idx)
            recommended_movies_ids.add(movie_tconst)

    if len(filtered_movies) == 0:
        return pd.DataFrame()  # Retourner un DataFrame vide si aucun film n'est trouvé

    # Récupérer les films similaires filtrés
    similar_movies = df.loc[filtered_movies]

    return similar_movies

# Page des recommandations de films
def movies_recommendation_page(df, cosine_sim):
    selected_movie_title = st.selectbox('Choisissez un film', [''] + list(df['Titres'].unique()), index=0)
    if selected_movie_title:
        movie_records = df[df['Titres'] == selected_movie_title]
        if not movie_records.empty:
            selected_movie_record = movie_records.iloc[0]
            selected_movie_id = selected_movie_record.name
            selected_movie_year = selected_movie_record['startYear']  # Récupération de l'année du film

            # Affichage des détails du film sélectionné avec style
            st.markdown("<h2 style='text-align: center; font-weight: bold; text-decoration: underline;'>Détails du film sélectionné</h2>", unsafe_allow_html=True)
            display_movie_details(selected_movie_record)

            # Affichage des films recommandés avec style
            st.markdown(f"<h2 style='text-align: center; font-weight: bold; text-decoration: underline;'>10 Films recommandés (entre {selected_movie_year - 5} et {selected_movie_year + 5})</h2>", unsafe_allow_html=True)
            recommended_movies = recommend_movies(selected_movie_id, df, cosine_sim)
            if not recommended_movies.empty:
                for _, movie in recommended_movies.iterrows():
                    display_movie_details(movie)
            else:
                st.write("Aucune recommandation disponible pour ce film.")

# Page des acteurs et actrices
def actors_page(df):
    actor_columns = ['actor_1', 'actor_2', 'actor_3', 'actor_4', 'actor_5', 'actress_1', 'actress_2', 'actress_3', 'actress_4', 'actress_5']
    all_actors = pd.unique(df[actor_columns].values.ravel('K'))
    all_actors = [actor for actor in all_actors if actor and actor != 'nan']

    selected_actor = st.selectbox('Choisissez un acteur ou une actrice', [''] + sorted(all_actors))
    if selected_actor:
        actor_movies = df[df[actor_columns].apply(lambda x: selected_actor in x.values, axis=1)].drop_duplicates(subset='tconst')
        actor_movies = actor_movies.sort_values(by='averageRating', ascending=False).head(20)

        st.markdown(f"<h2 style='text-align: center; font-weight: bold;'>Le(s) film(s) avec {selected_actor} le(s) plus plébiscité(s) sur le site IMDB</h2>", unsafe_allow_html=True)
        for _, movie in actor_movies.iterrows():
            display_movie_details(movie)

# Nouvelle page pour les réalisateurs
def directors_page(df):
    director_columns = ['director_1', 'director_2', 'director_3', 'director_4', 'director_5']
    all_directors = pd.unique(df[director_columns].values.ravel('K'))
    all_directors = [director for director in all_directors if director and director != 'nan']

    selected_director = st.selectbox('Choisissez un réalisateur', [''] + sorted(all_directors))
    
    if selected_director:
        director_movies = df[df[director_columns].apply(lambda x: selected_director in x.values, axis=1)].drop_duplicates(subset='tconst')
        director_movies = director_movies.sort_values(by='averageRating', ascending=False).head(20)

        st.markdown(f"<h2 style='text-align: center; font-weight: bold;'>Film(s) réalisé(s) par {selected_director} le(s) plus plébiscité(s) sur le site IMDB</h2>", unsafe_allow_html=True)
        for _, movie in director_movies.iterrows():
            display_movie_details(movie)

# Page pour les genres
def genres_page(df):
    genre_columns = ['genres_1', 'genres_2', 'genres_3']
    all_genres = pd.unique(df[genre_columns].values.ravel('K'))
    all_genres = [genre for genre in all_genres if genre and genre != 'nan']

    selected_genre = st.selectbox('Choisissez un genre', [''] + sorted(all_genres))
    
    if selected_genre:
        genre_movies = df[df[genre_columns].apply(lambda x: selected_genre in x.values, axis=1)]
        genre_movies = genre_movies.drop_duplicates(subset='tconst')

        # Filtrer les films avec au moins 100000 votes et trier par averageRating
        genre_movies = genre_movies[genre_movies['numVotes'] >= 100000]
        genre_movies = genre_movies.sort_values(by='averageRating', ascending=False).head(20)

        st.markdown(f"<h2 style='text-align: center; font-weight: bold; text-decoration: underline;'>Top des films du genre {selected_genre} les plus plébiscités sur le site IMDB</h2>", unsafe_allow_html=True)
        for _, movie in genre_movies.iterrows():
            display_movie_details(movie)

# Page du Top 100 des films
def top_movies_page(df):
    # Filtrer les films avec au moins 100000 votes et supprimer les doublons
    top_movies = df[df['numVotes'] >= 100000].drop_duplicates(subset='tconst')

    # Trier les films par averageRating dans l'ordre décroissant et limiter à 100 films
    top_movies = top_movies.sort_values(by='averageRating', ascending=False).head(100)

    st.markdown("<h2 style='text-align: center; font-weight: bold; text-decoration: underline;'>Top 100 des films les plus plébiscités sur le site IMDB</h2>", unsafe_allow_html=True)
    for _, movie in top_movies.iterrows():
        display_movie_details(movie)

# Page de connexion pour Power BI
def power_bi_login_page():
    st.markdown("<h2 style='text-align: center; font-weight: bold; text-decoration: underline;'>Connexion Power BI</h2>", unsafe_allow_html=True)
    
    username = st.text_input("Nom utilisateur")
    password = st.text_input("Mot de passe", type='password')

    # Informations de connexion prédéfinies
    correct_username = "videodrome"
    correct_password = "123"

    # Bouton de connexion
    submit_button = st.button("Connexion")

    if submit_button:
        if username == correct_username and password == correct_password:
            st.success("Connexion réussie")
            # URL du tableau Power BI
            power_bi_url = "https://app.powerbi.com/groups/me/reports/29ececc9-1ae3-408c-a625-0f324ede06fa/ReportSection7125f52527d5bcb06d9a?experience=power-bi"  # Remplacez par l'URL de votre tableau Power BI
            st.markdown(f"[Ouvrir Power BI]({power_bi_url})", unsafe_allow_html=True)
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect")

# Interface utilisateur Streamlit
def main():
    st.markdown("<h1 style='text-align: center; text-decoration: underline;'>VIDEODROME - Recommandations de films</h1>", unsafe_allow_html=True)
    
    df, cosine_sim = load_and_prepare_data()  # Correction ici pour correspondre au retour de la fonction

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Recommandations de films", "Acteurs et Actrices", "Réalisateurs", "Genres", "Top 100 des Films", "Dashboard"])

    with tab1:
        movies_recommendation_page(df, cosine_sim)  # Mise à jour pour correspondre à la nouvelle signature

    with tab2:
        actors_page(df)

    with tab3:
        directors_page(df)

    with tab4:
        genres_page(df)

    with tab5:
        top_movies_page(df)

    with tab6:
        power_bi_login_page()

main()
