# recommendation_engine.py
import pandas as pd
import numpy as np
import random # For shuffling recommendations
import warnings

warnings.filterwarnings('ignore')

class MoodBasedRecommender:
    MOOD_GENRE_MAP = {
        "Happy": ["Comedy", "Adventure", "Family", "Animation"],
        "Sad": ["Drama", "Romance", "Music"],
        "Excited": ["Action", "Thriller", "Sci-Fi", "Adventure"],
        "Romantic": ["Romance", "Drama", "Musical"],
        "Relaxed": ["Documentary", "Animation", "Family", "Fantasy"],
        "Inspired": ["Biography", "Drama", "History"],
        "Scared": ["Horror", "Thriller", "Mystery"],
        "Thoughtful": ["Drama", "Mystery", "Sci-Fi", "Thriller"],
        "Funny": ["Comedy", "Family"],
        "Adventurous": ["Adventure", "Action", "Fantasy", "Sci-Fi"],
        "Nostalgic": ["Drama", "Romance", "Family", "History"],
        "Curious": ["Documentary", "Mystery", "Sci-Fi"]
    }

    def __init__(self, data_handler):
        self.movies_df = data_handler.movies_df
        print("MoodBasedRecommender initialized with imdb_movies.csv data.")

    def get_movies_by_mood(self, mood, n_recommendations=10):
        """
        Recommends movies based on the selected mood by filtering genres.
        Uses 'genres' column from imdb_movies.csv.
        """
        target_genres = self.MOOD_GENRE_MAP.get(mood, [])

        if not target_genres:
            print(f"No genres mapped for mood '{mood}'. Returning popular movies.")
            return self.get_popular_movies(n_recommendations)

        genre_pattern = '|'.join(target_genres)
        
        # Ensure 'genres' column is treated as string for regex and filter
        # The 'genres' column is created in data_handler.py from 'genre'
        filtered_movies = self.movies_df[
            self.movies_df['genres'].astype(str).str.contains(genre_pattern, case=False, na=False)
        ]

        if filtered_movies.empty:
            print(f"No movies found for genres associated with mood '{mood}'. Returning popular movies.")
            return self.get_popular_movies(n_recommendations)

        # Sort by 'score' (IMDb rating) to prioritize better-rated movies within the mood
        # Then shuffle to add some randomness among equally scored movies
        recommended_movies = filtered_movies.sort_values(by='score', ascending=False).sample(frac=1, random_state=42).reset_index(drop=True)
        
        top_movies = recommended_movies.head(n_recommendations)

        formatted_recommendations = []
        for _, row in top_movies.iterrows():
            formatted_recommendations.append({
                'movieId': row['movieId'],
                'title': row['title'],
                'genres': row['genres'],
                'score': row['score'] # Use the 'score' from imdb_movies.csv
            })
        
        print(f"Found {len(formatted_recommendations)} movies for mood '{mood}'.")
        return formatted_recommendations

    def get_popular_movies(self, n_recommendations=10):
        """
        Gets popular movies based on the 'score' column from imdb_movies.csv.
        """
        if self.movies_df.empty:
            print("Movies DataFrame is empty. Cannot get popular movies.")
            return []

        # Sort by 'score' (IMDb rating) to get truly popular movies
        popular_movies = self.movies_df.sort_values(by='score', ascending=False).head(n_recommendations)

        formatted_recommendations = []
        for _, row in popular_movies.iterrows():
            formatted_recommendations.append({
                'movieId': row['movieId'],
                'title': row['title'],
                'genres': row['genres'],
                'score': row['score'] # Use the 'score' from imdb_movies.csv
            })
        print(f"Returning {len(formatted_recommendations)} popular movies.")
        return formatted_recommendations
