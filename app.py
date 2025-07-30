import pickle
import streamlit as st
import requests
import pandas as pd
import random

# Load data and model from Hugging Face
movies_url = "https://huggingface.co/datasets/ChaitanyaChu/movie-recommender-data/resolve/main/movies_rec.pkl"
similarity_url = "https://huggingface.co/datasets/ChaitanyaChu/movie-recommender-data/resolve/main/similarity.pkl"

movies = pickle.loads(requests.get(movies_url).content)
similarity = pickle.loads(requests.get(similarity_url).content)

# Fetching poster from TMDB API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    data = response.json()
    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "https://via.placeholder.com/300x450?text=No+Image"

# Recommendation Logic
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_ids = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommended_movie_ids.append(movie_id)
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names, recommended_movie_posters, recommended_movie_ids

# Page Config
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

# CSS Styling
st.markdown("""
    <style>
        html, body, .stApp {
            background-color: #141414;
            color: #ffffff;
            font-family: 'Helvetica Neue', sans-serif;
        }
        h1, h2, h3 {
            color: #e50914;
        }
        .stSelectbox label, .stTextInput label {
            color: #ffffff !important;
        }
        .stButton>button {
            background-color: #e50914;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 0.5em 1em;
            font-weight: bold;
        }
        .movie-title {
            font-weight: bold;
            text-align: center;
            color: #ffffff;
            margin-top: 0.5rem;
        }
    </style>
""", unsafe_allow_html=True)

# Streamlit UI
st.title('🍿 Movie Recommender System')

# Random Movies Display
st.markdown("## 🔥 Random Movie Picks")
random_movies = movies.sample(10).reset_index(drop=True)
cols = st.columns(len(random_movies))

for i, row in random_movies.iterrows():
    with cols[i]:
        poster = fetch_poster(row['id'])
        tmdb_link = f"https://www.themoviedb.org/movie/{row['id']}"
        st.markdown(f"""
            <a href="{tmdb_link}" target="_blank">
                <img src="{poster}" style="width:100%; border-radius:10px;" />
            </a>
            <div class='movie-title'>{row['title']}</div>
        """, unsafe_allow_html=True)

# Input for Recommendation
st.markdown("## 🔍 Get Movie Recommendations")
selected_movie = st.selectbox("🎯 Pick a movie you like:", movies['title'].values)

if st.button('🎯 Recommend Similar Movies'):
    names, posters, ids = recommend(selected_movie)
    st.markdown("### 🎥 You Might Also Like:")
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            link = f"https://www.themoviedb.org/movie/{ids[i]}"
            st.markdown(f"""
                <a href="{link}" target="_blank">
                    <img src="{posters[i]}" style="width:100%; border-radius:10px;" />
                </a>
                <div class='movie-title'>{names[i]}</div>
            """, unsafe_allow_html=True)
