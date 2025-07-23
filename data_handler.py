# data_handler.py
import pandas as pd
import numpy as np
import os
import warnings

warnings.filterwarnings('ignore')

class MovieDataHandler:
    def __init__(self):
        self.movies_df = None
        self.data_folder = 'movie_data'
        self.imdb_movies_filename = 'imdb_movies.csv'
        self.bollywood_movies_filename = 'bollywood_movies.csv'

    # This method is no longer needed for custom datasets
    def download_movielens_data(self):
        """This method is deprecated as we are using local custom datasets.
        Please ensure 'imdb_movies.csv' and 'bollywood_movies.csv' are in the 'movie_data' folder."""
        print("Using custom datasets. Skipping MovieLens download.")
        return self.data_folder

    def load_data(self):
        """Load and combine movie data from imdb_movies.csv and bollywood_movies.csv."""
        imdb_movies_path = os.path.join(self.data_folder, self.imdb_movies_filename)
        bollywood_movies_path = os.path.join(self.data_folder, self.bollywood_movies_filename)

        # --- Load and process IMDb movies ---
        if not os.path.exists(imdb_movies_path):
            raise FileNotFoundError(f"IMDb dataset file '{imdb_movies_path}' not found. Please check its location.")
        print(f"Loading IMDb movies from '{imdb_movies_path}'...")
        imdb_df = pd.read_csv(imdb_movies_path, low_memory=False)

        # Preprocessing for IMDb movies
        if 'names' in imdb_df.columns:
            imdb_df.rename(columns={'names': 'title'}, inplace=True)
        imdb_df.dropna(subset=['title'], inplace=True)
        imdb_df = imdb_df[imdb_df['title'].astype(bool)]

        imdb_df['genre'] = imdb_df['genre'].fillna('')
        imdb_df['genres'] = imdb_df['genre'].apply(lambda x: x.replace(', ', '|') if isinstance(x, str) else '')
        if 'genre' in imdb_df.columns:
            imdb_df.drop(columns=['genre'], inplace=True)

        imdb_df['movieId'] = imdb_df.index # Assign unique IDs
        imdb_df['score'] = pd.to_numeric(imdb_df['score'], errors='coerce').fillna(0) # IMDb score
        imdb_df['source'] = 'IMDb' # Add source column

        # Select relevant columns for IMDb movies
        imdb_df = imdb_df[['movieId', 'title', 'genres', 'score', 'source']]

        # --- Load and process Bollywood movies ---
        if not os.path.exists(bollywood_movies_path):
            raise FileNotFoundError(f"Bollywood dataset file '{bollywood_movies_path}' not found. Please check its location.")
        print(f"Loading Bollywood movies from '{bollywood_movies_path}'...")
        bollywood_df = pd.read_csv(bollywood_movies_path, low_memory=False)

        # Preprocessing for Bollywood movies
        bollywood_df.rename(columns={'Movie Name': 'title', 'Genre': 'genres'}, inplace=True)
        bollywood_df.dropna(subset=['title'], inplace=True)
        bollywood_df = bollywood_df[bollywood_df['title'].astype(bool)]

        # Convert comma-separated genres to pipe-separated
        bollywood_df['genres'] = bollywood_df['genres'].fillna('')
        bollywood_df['genres'] = bollywood_df['genres'].apply(lambda x: x.replace(', ', '|') if isinstance(x, str) else '')

        # Use 'Revenue(INR)' as a proxy for score, fill NaN with 0
        bollywood_df['score'] = pd.to_numeric(bollywood_df['Revenue(INR)'], errors='coerce').fillna(0)
        
        # Generate unique movieId for Bollywood movies, offset from IMDb movies
        # Ensure IDs are unique across both datasets
        max_imdb_id = imdb_df['movieId'].max() if not imdb_df.empty else -1
        bollywood_df['movieId'] = bollywood_df.index + max_imdb_id + 1
        bollywood_df['source'] = 'Bollywood' # Add source column

        # Select relevant columns for Bollywood movies
        bollywood_df = bollywood_df[['movieId', 'title', 'genres', 'score', 'source']]

        # --- Combine both datasets ---
        self.movies_df = pd.concat([imdb_df, bollywood_df], ignore_index=True)

        print(f"Loaded {len(imdb_df)} IMDb movies and {len(bollywood_df)} Bollywood movies.")
        print(f"Combined dataset has {len(self.movies_df)} movies.")
        return self.movies_df # Only return the combined movies_df
