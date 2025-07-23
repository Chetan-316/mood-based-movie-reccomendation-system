import pandas as pd
import numpy as np
import os
import warnings

warnings.filterwarnings('ignore')

class MovieDataHandler:
    def __init__(self, imdb_movies_filename='imdb_movies.csv', bollywood_movies_filename='bollywood_movies.csv'):
        self.movies_df = None
        self.imdb_movies_filename = imdb_movies_filename
        self.bollywood_movies_filename = bollywood_movies_filename

    def load_data(self):
        """Load and combine movie data from imdb_movies.csv and bollywood_movies.csv placed in root folder."""

        # Paths assume the CSVs are in the root directory
        imdb_movies_path = os.path.join(self.imdb_movies_filename)
        bollywood_movies_path = os.path.join(self.bollywood_movies_filename)

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

        imdb_df['movieId'] = imdb_df.index  # Assign unique IDs

        # Ensure 'score' column exists
        if 'score' not in imdb_df.columns:
            imdb_df['score'] = np.random.uniform(5.0, 9.0, size=len(imdb_df))  # Generate random scores
        else:
            imdb_df['score'] = pd.to_numeric(imdb_df['score'], errors='coerce').fillna(5.0)

        imdb_df['source'] = 'IMDb'

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

        bollywood_df['genres'] = bollywood_df['genres'].fillna('')
        bollywood_df['genres'] = bollywood_df['genres'].apply(lambda x: x.replace(', ', '|') if isinstance(x, str) else '')

        # Ensure 'score' column exists
        if 'Revenue(INR)' not in bollywood_df.columns:
            bollywood_df['score'] = np.random.uniform(5.0, 9.0, size=len(bollywood_df))  # Random scores
        else:
            bollywood_df['score'] = pd.to_numeric(bollywood_df['Revenue(INR)'], errors='coerce').fillna(5.0)

        bollywood_df['movieId'] = bollywood_df.index + imdb_df['movieId'].max() + 1
        bollywood_df['source'] = 'Bollywood'

        bollywood_df = bollywood_df[['movieId', 'title', 'genres', 'score', 'source']]

        # --- Combine datasets ---
        self.movies_df = pd.concat([imdb_df, bollywood_df], ignore_index=True)

        print(f"✅ Loaded {len(imdb_df)} IMDb movies and {len(bollywood_df)} Bollywood movies.")
        print(f"✅ Combined dataset has {len(self.movies_df)} movies.")
        return self.movies_df
