# data_handler.py
import pandas as pd
import numpy as np
import os
import warnings

warnings.filterwarnings('ignore')

class MovieDataHandler:
    def __init__(self):
        self.movies_df = None
        # Define the folder and filename for your custom dataset
        self.data_folder = 'movie_data'
        self.imdb_movies_filename = 'imdb_movies.csv'

    # This method is no longer needed for a custom downloaded dataset like imdb_movies.csv
    def download_movielens_data(self):
        """This method is deprecated as we are using a local custom dataset.
        Please ensure 'imdb_movies.csv' is in the 'movie_data' folder."""
        print("Using custom dataset. Skipping MovieLens download.")
        return self.data_folder

    def load_data(self):
        """Load custom movie data from imdb_movies.csv."""
        imdb_movies_path = os.path.join(self.data_folder, self.imdb_movies_filename)

        if not os.path.exists(imdb_movies_path):
            print(f"Error: Missing dataset file '{imdb_movies_path}'.")
            print(f"Please ensure '{self.imdb_movies_filename}' is in the '{self.data_folder}' folder.")
            raise FileNotFoundError(f"Dataset file '{self.imdb_movies_filename}' not found. Please check its location.")

        print(f"Loading custom dataset from '{imdb_movies_path}'...")

        # Load movies data
        # low_memory=False helps avoid DtypeWarning for mixed types in columns
        self.movies_df = pd.read_csv(imdb_movies_path, low_memory=False)

        # --- Data Cleaning and Preprocessing for imdb_movies.csv ---

        # 1. Rename 'names' column to 'title'
        if 'names' in self.movies_df.columns:
            self.movies_df.rename(columns={'names': 'title'}, inplace=True)
        else:
            print("Warning: 'names' column not found. Assuming 'title' is already correct.")

        # Ensure 'title' column exists and is not empty
        self.movies_df.dropna(subset=['title'], inplace=True)
        self.movies_df = self.movies_df[self.movies_df['title'].astype(bool)] # Remove empty strings

        # 2. Handle 'genre' column: It's comma-separated, convert to pipe-separated for consistency
        # Fill NaN with empty string before processing
        self.movies_df['genre'] = self.movies_df['genre'].fillna('')
        self.movies_df['genres'] = self.movies_df['genre'].apply(lambda x: x.replace(', ', '|') if isinstance(x, str) else '')
        # Drop the original 'genre' column if 'genres' is successfully created
        if 'genre' in self.movies_df.columns:
            self.movies_df.drop(columns=['genre'], inplace=True)

        # 3. Create a unique 'movieId' for each movie
        # Since imdb_movies.csv doesn't have a direct movieId for collaborative filtering,
        # we'll use the DataFrame's internal index as a unique ID.
        self.movies_df['movieId'] = self.movies_df.index

        # 4. Ensure 'score' column (for popularity) is numeric
        # Fill any non-numeric scores with 0 or NaN, then fill NaN with 0
        self.movies_df['score'] = pd.to_numeric(self.movies_df['score'], errors='coerce').fillna(0)

        # Optional: Reduce dataset size for memory optimization if needed
        # The imdb_movies.csv has ~10k movies, which might still be large for similarity matrices
        # For mood-based, we don't build a similarity matrix, so this might not be strictly necessary
        # but if you later add content-based features, keep this in mind.
        # For now, we'll load all of it as we're not building a large similarity matrix.

        print(f"Loaded {len(self.movies_df)} movies from custom dataset.")
        return self.movies_df # Only return movies_df
