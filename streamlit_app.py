# streamlit_app.py
import streamlit as st
import pandas as pd
import numpy as np
from data_handler import MovieDataHandler
from recommendation_engine import MoodBasedRecommender
from omdb_api import OMDbAPI
from dotenv import load_dotenv
import time # For st.spinner delay

load_dotenv() # Load environment variables from .env file

# Set page config
st.set_page_config(
    page_title="Mood-Based Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

# Initialize session state variables
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
    st.session_state.data_handler = None
    st.session_state.recommender = None

@st.cache_data
def load_data():
    """Load and process data for mood-based filtering."""
    data_handler = MovieDataHandler()
    # This will load imdb_movies.csv
    movies_df = data_handler.load_data()
    return data_handler

@st.cache_resource
# Fixed UnhashableParamError by adding an underscore to the parameter name
def initialize_recommender(_data_handler):
    """Initialize mood-based recommendation engine."""
    return MoodBasedRecommender(_data_handler)

def main():
    st.title("🎬 Mood-Based Movie Recommendation System")
    st.sidebar.title("Navigation")

    # Load data and initialize recommender
    if not st.session_state.data_loaded:
        with st.spinner("Loading movie data from imdb_movies.csv and initializing system..."): # ✅ Changed message
            st.session_state.data_handler = load_data()
            st.session_state.recommender = initialize_recommender(st.session_state.data_handler)
            st.session_state.data_loaded = True

    # OMDb API setup
    omdb_api = OMDbAPI()

    # Mood selection dropdown
    mood_options = list(MoodBasedRecommender.MOOD_GENRE_MAP.keys())
    selected_mood = st.sidebar.selectbox(
        "Select your current mood:",
        mood_options
    )

    n_recommendations = st.sidebar.slider(
        "Number of Recommendations:",
        min_value=3,
        max_value=15,
        value=6 # Default to 6 recommendations for a 3-column grid
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Dataset Info")
    if st.session_state.data_loaded:
        st.sidebar.write(f"Total Movies: {len(st.session_state.data_handler.movies_df)}")

    st.header(f"Movies for a '{selected_mood}' Mood:")

    if st.button(f"Get Recommendations for {selected_mood}"):
        with st.spinner("Finding movies that match your mood..."):
            recommendations = st.session_state.recommender.get_movies_by_mood(
                selected_mood, n_recommendations
            )
            display_recommendations(recommendations, omdb_api)

    # Optional: Display popular movies as a general option
    st.markdown("---")
    st.subheader("Or, just some popular movies:")
    if st.button("Show Popular Movies"):
        with st.spinner("Fetching popular movies..."):
            popular_recommendations = st.session_state.recommender.get_popular_movies(n_recommendations)
            display_recommendations(popular_recommendations, omdb_api)


def display_recommendations(recommendations, omdb_api):
    """Display recommendations with posters and details fetched from OMDb API."""
    if not recommendations:
        st.warning("No recommendations found for this mood. Try a different mood or show popular movies.")
        return

    st.markdown("---")
    # Create columns for grid layout (3 columns for better visual appeal)
    cols = st.columns(3)

    for i, movie in enumerate(recommendations):
        col = cols[i % 3] # Distribute movies across columns

        with col:
            # Fetch detailed info and poster from OMDb API
            # Use st.cache_data for OMDb API calls to avoid re-fetching on every rerun
            @st.cache_data(show_spinner=False)
            def get_omdb_details_cached(title):
                return omdb_api.get_movie_details(title)

            omdb_details = get_omdb_details_cached(movie['title'])

            st.markdown(f"**{movie['title']}**")
            st.markdown(f"*Genres: {movie['genres']}*")

            if omdb_details:
                st.markdown(f"*IMDb Rating: {omdb_details.get('rating', 'N/A')}*")
                poster_url = omdb_details.get('poster_url', "https://via.placeholder.com/500x750?text=No+Image")
                st.image(poster_url, width=200, caption=movie['title'])
            else:
                st.markdown(f"*IMDb Rating: {movie.get('score', 'N/A')}* (from dataset)") # Use dataset score if OMDb fails
                st.image("https://via.placeholder.com/500x750?text=No+Image", width=200, caption="No Poster")
                st.markdown("*Details not available from OMDb.*")
            
            st.markdown("---") # Separator for each movie

if __name__ == "__main__":
    main()
