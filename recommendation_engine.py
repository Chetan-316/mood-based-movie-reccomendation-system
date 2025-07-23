# recommendation_engine.py
import pandas as pd
import numpy as np
import random
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
        "Thoughtful": ["Drama", "Mystery", "Sci-Fi"],
        "Funny": ["Comedy", "Family"],
        "Adventurous": ["Adventure", "Action", "Fantasy", "Sci-Fi"],
        "Nostalgic": ["Drama", "Romance", "Family", "History"],
        "Curious": ["Documentary", "Mystery", "Sci-Fi"]
    }

    def __init__(self, data_handler):
        self.movies_df = data_handler.movies_df.copy()

        # 🛠️ Fix: Replace missing scores with random values
        self.movies_df['score'] = self.movies_df['score'].apply(
            lambda x: x if pd.notnull(x) else np.random.uniform(1, 10)
        )

        print("✅ MoodBasedRecommender initialized with combined movie data.")

    def _filter_by_industry(self, df, industry):
        """Helper to filter DataFrame by 'source' (industry)."""
        if industry == "Hollywood":
            return df[df['source'] == 'IMDb']
        elif industry == "Bollywood":
            return df[df['source'] == 'Bollywood']
        else:  # "All" or any other value
            return df

    def get_movies_by_mood(self, mood, n_recommendations=10, industry="All"):
        """
        Recommends movies based on the selected mood and industry.
        """
        target_genres = self.MOOD_GENRE_MAP.get(mood, [])

        if not target_genres:
            print(f"⚠️ No genres mapped for mood '{mood}'. Returning popular movies instead.")
            return self.get_popular_movies(n_recommendations, industry=industry)

        genre_pattern = '|'.join(target_genres)

        filtered_movies = self.movies_df[
            self.movies_df['genres'].astype(str).str.contains(genre_pattern, case=False, na=False)
        ]

        # Apply industry filter
        filtered_movies = self._filter_by_industry(filtered_movies, industry)

        if filtered_movies.empty:
            print(f"⚠️ No movies found for mood '{mood}' in '{industry}'. Returning popular movies.")
            return self.get_popular_movies(n_recommendations, industry=industry)

        recommended_movies = (
            filtered_movies.sort_values(by='score', ascending=False)
            .sample(frac=1, random_state=42)
            .reset_index(drop=True)
        )

        top_movies = recommended_movies.head(n_recommendations)

        formatted_recommendations = [
            {
                'movieId': row['movieId'],
                'title': row['title'],
                'genres': row['genres'],
                'score': row['score'],
                'source': row['source']
            }
            for _, row in top_movies.iterrows()
        ]

        print(f"🎉 Found {len(formatted_recommendations)} movies for mood '{mood}'.")
        return formatted_recommendations

    def get_popular_movies(self, n_recommendations=10, industry="All"):
        """Gets popular movies based on the 'score' column, filtered by industry."""
        if self.movies_df.empty:
            print("⚠️ Movies DataFrame is empty.")
            return []

        movies_to_consider = self._filter_by_industry(self.movies_df, industry)

        if movies_to_consider.empty:
            print(f"⚠️ No movies found for industry '{industry}'.")
            return []

        popular_movies = (
            movies_to_consider.sort_values(by='score', ascending=False)
            .head(n_recommendations)
        )

        formatted_recommendations = [
            {
                'movieId': row['movieId'],
                'title': row['title'],
                'genres': row['genres'],
                'score': row['score'],
                'source': row['source']
            }
            for _, row in popular_movies.iterrows()
        ]

        print(f"🎬 Returning {len(formatted_recommendations)} popular movies for '{industry}'.")
        return formatted_recommendations
