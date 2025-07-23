# streamlit_app.py

import streamlit as st
import pandas as pd
import numpy as np
from data_handler import MovieDataHandler
from recommendation_engine import MoodBasedRecommender
from omdb_api import OMDbAPI
from dotenv import load_dotenv
import time

load_dotenv()  # Load environment variables from .env file

# Set page config
st.set_page_config(
    page_title="🎬 CineMood: Mood-Based Movie Recommendations",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 Advanced Cinematic UI
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background: #0a0e1a;
        color: #ffffff;
        scroll-behavior: smooth;
    }
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #1a1f2e 25%, #2d1b3d 50%, #1a1f2e 75%, #0a0e1a 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(45deg, #ff6b6b, #48dbfb, #feca57, #ff9ff3);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientText 8s ease infinite;
        margin: 1rem 0;
    }
    @keyframes gradientText {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    </style>
""", unsafe_allow_html=True)


# ✅ Debug: Track state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
    st.session_state.data_handler = None
    st.session_state.recommender = None


@st.cache_data
def load_data():
    """Load and process data for mood-based filtering."""
    print("✅ Loading dataset...")
    try:
        data_handler = MovieDataHandler()
        df = data_handler.load_data()
        print(f"✅ Loaded {len(df)} movies.")
        return data_handler
    except Exception as e:
        print(f"❌ Failed to load data: {e}")
        # Provide fallback
        fallback_data = pd.DataFrame({
            "title": ["Inception", "3 Idiots", "The Dark Knight", "Dil Chahta Hai"],
            "genres": ["Action|Sci-Fi", "Comedy|Drama", "Action|Thriller", "Drama|Romance"],
            "source": ["IMDb", "Bollywood", "IMDb", "Bollywood"]
        })
        data_handler = MovieDataHandler()
        data_handler.movies_df = fallback_data
        return data_handler


@st.cache_resource
def initialize_recommender(_data_handler):
    """Initialize mood-based recommendation engine."""
    print("✅ Initializing recommender...")
    return MoodBasedRecommender(_data_handler)


def main():
    st.markdown('<h1 class="main-title">🎬 CineMood</h1>', unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>Discover movies that perfectly match your mood</h4>", unsafe_allow_html=True)

    # Load data
    if not st.session_state.data_loaded:
        with st.spinner("🎞️ Loading movies..."):
            st.session_state.data_handler = load_data()
            st.session_state.recommender = initialize_recommender(st.session_state.data_handler)
            st.session_state.data_loaded = True

    omdb_api = OMDbAPI()

    # Sidebar
    st.sidebar.header("🎭 Select Mood")
    mood_options = list(MoodBasedRecommender.MOOD_GENRE_MAP.keys())
    selected_mood = st.sidebar.selectbox("How are you feeling today?", mood_options)

    n_recommendations = st.sidebar.slider(
        "Number of Recommendations",
        min_value=3, max_value=12, value=6
    )

    st.sidebar.markdown("---")
    st.sidebar.info("💡 Tip: Select a mood to discover matching movies.")

    # Main recommendations section
    if st.button(f"🍿 Recommend {selected_mood} Movies"):
        with st.spinner("🎥 Fetching movie recommendations..."):
            recommendations = st.session_state.recommender.get_movies_by_mood(
                selected_mood, n_recommendations
            )
            display_recommendations(recommendations, omdb_api)


def display_recommendations(recommendations, omdb_api):
    """Display recommendations in a grid."""
    if not recommendations:
        st.warning("😕 No movies found. Try a different mood.")
        return

    cols = st.columns(3)

    for i, movie in enumerate(recommendations):
        col = cols[i % 3]
        with col:
            st.markdown(f"**🎬 {movie['title']}**")
            st.markdown(f"*Genres:* {movie['genres'].replace('|', ', ')}")
            details = omdb_api.get_movie_details(movie['title'])
            poster = details.get("poster_url") if details else None
            if poster and poster != "N/A":
                st.image(poster, use_container_width=True)  # ✅ Updated parameter
            else:
                st.image("https://via.placeholder.com/300x450?text=No+Image", use_container_width=True)
            rating = details.get("rating") if details else "N/A"
            st.markdown(f"⭐ IMDb Rating: {rating}")


if __name__ == "__main__":
    main()
