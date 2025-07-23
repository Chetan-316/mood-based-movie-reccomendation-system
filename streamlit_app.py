# streamlit_app.py

import streamlit as st
import pandas as pd
import numpy as np
from data_handler import MovieDataHandler
from recommendation_engine import MoodBasedRecommender
from omdb_api import OMDbAPI
from dotenv import load_dotenv

load_dotenv()

# 🎨 Page Config
st.set_page_config(
    page_title="🎬 CineMood: Mood-Based Movie Recommendations",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🌈 Advanced UI
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background: #0a0e1a;
        color: #ffffff;
    }
    .stApp {
        background: linear-gradient(135deg, #0a0e1a, #1a1f2e, #2d1b3d, #1a1f2e, #0a0e1a);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    .movie-title {
        font-weight: bold;
        font-size: 1.3rem;
        color: #feca57;
        text-shadow: 0 0 5px #000;
        margin-bottom: 0.3rem;
    }
    </style>
""", unsafe_allow_html=True)

# ✅ State initialization
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
    st.session_state.data_handler = None
    st.session_state.recommender = None


@st.cache_data
def load_data():
    """Load dataset."""
    try:
        data_handler = MovieDataHandler()
        df = data_handler.load_data()
        return data_handler
    except Exception as e:
        print(f"⚠️ Data load failed: {e}")
        fallback_data = pd.DataFrame({
            "title": ["Inception", "3 Idiots", "The Dark Knight", "Dil Chahta Hai"],
            "genres": ["Action|Sci-Fi", "Comedy|Drama", "Action|Thriller", "Drama|Romance"],
            "source": ["IMDb", "Bollywood", "IMDb", "Bollywood"],
            "score": [8.8, 8.4, 9.0, 8.1]  # ✅ Added fallback scores
        })
        data_handler = MovieDataHandler()
        data_handler.movies_df = fallback_data
        return data_handler


@st.cache_resource
def initialize_recommender(_data_handler):
    return MoodBasedRecommender(_data_handler)


def main():
    st.title("🎬 CineMood")
    st.caption("Discover movies that perfectly match your mood 🎭")

    if not st.session_state.data_loaded:
        with st.spinner("🎞 Loading movies..."):
            st.session_state.data_handler = load_data()
            st.session_state.recommender = initialize_recommender(st.session_state.data_handler)
            st.session_state.data_loaded = True

    omdb_api = OMDbAPI()

    st.sidebar.header("🎭 Select Mood")
    mood_options = list(MoodBasedRecommender.MOOD_GENRE_MAP.keys())
    selected_mood = st.sidebar.selectbox("How are you feeling today?", mood_options)

    n_recommendations = st.sidebar.slider(
        "Number of Recommendations", min_value=3, max_value=12, value=6
    )

    if st.button(f"🍿 Recommend {selected_mood} Movies"):
        with st.spinner("🎥 Fetching recommendations..."):
            recommendations = st.session_state.recommender.get_movies_by_mood(
                selected_mood, n_recommendations
            )
            display_recommendations(recommendations, omdb_api)


def display_recommendations(recommendations, omdb_api):
    """Show recommendations in a grid."""
    if not recommendations:
        st.warning("😕 No movies found. Try a different mood.")
        return

    cols = st.columns(3)

    for i, movie in enumerate(recommendations):
        col = cols[i % 3]
        with col:
            st.markdown(f"<div class='movie-title'>🎬 {movie['title']}</div>", unsafe_allow_html=True)
            st.markdown(f"*Genres:* {movie['genres'].replace('|', ', ')}")
            details = omdb_api.get_movie_details(movie['title'])
            poster = details.get("poster_url") if details else None
            if poster and poster != "N/A":
                st.image(poster, use_container_width=True)
            else:
                st.image("https://via.placeholder.com/300x450?text=No+Image", use_container_width=True)
            rating = details.get("rating") if details else "N/A"
            st.markdown(f"⭐ IMDb Rating: {rating}")


if __name__ == "__main__":
    main()
