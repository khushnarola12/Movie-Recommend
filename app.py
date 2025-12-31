import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8"

    response = requests.get(url)

    if response.status_code != 200:
        return "https://via.placeholder.com/300x450?text=API+Error"

    data = response.json()

    if data.get("poster_path") is None:
        return "https://via.placeholder.com/300x450?text=No+Poster"

    return "https://image.tmdb.org/t/p/w500" + data["poster_path"]


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_movies_poster = []

    for i in movies_list:
        movie_row = movies.iloc[i[0]]

        movie_id = movie_row.movie_id  # ⚠️ OR movie_row.id

        recommended_movies.append(movie_row.title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster


movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("🎬 Movie Recommender System")

selected_movie_name = st.selectbox(
    "Select a movie",
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
