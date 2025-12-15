import streamlit as st
import pandas as pd
import pickle
import requests
import time
import os
import gdown

session = requests.Session()
session.headers.update({"User_Agent": "Movie/1.0"})
FOLDER_ID = "1XiuyMjclwaCy7bgMOiB9GZ0zix8XWG0D"

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {"api_key": "0f57ae1ee57ca4f85ca6fe7bf04f78bf", "language": "en-US"}
    for attempt in range(3):
        try:
            response = session.get(url, params=params, timeout=10)
            response.raise_for_status()
            response_data = response.json()
            poster_path = response_data.get("poster_path", None)
            return "https://image.tmdb.org/t/p/w500/" + response_data["poster_path"]
        except requests.exceptions.RequestException:
            if attempt < 2:
                time.sleep(1)
                continue
            raise


def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[
        1:6
    ]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


@st.cache_resource
def load_models():
    if not os.path.exists("movie_dict.pkl") or not os.path.exists("similarity.pkl"):
        gdown.download_folder(
            f"https://drive.google.com/drive/folders/{FOLDER_ID}",
            quiet=False,
            use_cookies=False,
        )


load_models()

movie_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))


st.title("Movie Recommendation System")

selected_movie_name = st.selectbox("Enter your favorite movie", movies["title"].values)

if st.button("Recommend"):
    name, poster = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(name[0])
        st.image(poster[0])

    with col2:
        st.text(name[1])
        st.image(poster[1])

    with col3:
        st.text(name[2])
        st.image(poster[2])

    with col4:
        st.text(name[3])
        st.image(poster[3])

    with col5:
        st.text(name[4])
        st.image(poster[4])
