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
        self.movies_df = data_handler.movies_df

        # ✅ Ensure 'score' column exists and has values
        if 'score' not in self.movies_df.columns:
            print("⚠️ 'score' column missing. Creating with random scores.")
            self.movies_df['score'] = np.random.uniform(5.0, 9.0, size=len(self.movies_df)).round(1)
        else:
            # Fill individual NaNs with random numbers (row-by-row)
            self.movies_df['score'] = self.movies_df['score'].apply(
                lambda x: x if pd.notnull(x) else round(random.uniform(5.0, 9.0), 1)
            )

        print("✅ MoodBasedRecommender initialized with movie data.")

    def _filter_by_industry(self, df, industry):
        """Filter DataFrame by 'source' (industry)."""
        if industry == "Hollywood":
            return df[df['source'] == 'IMDb']
        elif industry == "Bollywood":
            return df[df['source'] == 'Bollywood']
        return df

    def get_movies_by_mood(self, mood, n_recommendations=10, industry="All"):
        """Recommend movies based on mood and industry."""
        target_genres = self.MOOD_GENRE_MAP.get(mood, [])
        if not target_genres:
            print(f"⚠️ No genres mapped for mood '{mood}'. Returning popular movies.")
            return self.get_popular_movies(n_recommendations, industry=industry)

        genre_pattern = '|'.join(target_genres)
        filtered_movies = self.movies_df[
            self.movies_df['genres'].astype(str).str.contains(genre_pattern, case=False, na=False)
        ]
        filtered_movies = self._filter_by_industry(filtered_movies, industry)

        if filtered_movies.empty:
            print(f"⚠️ No movies found for '{mood}' in '{industry}'. Returning popular movies.")
            return self.get_popular_movies(n_recommendations, industry=industry)

        recommended_movies = filtered_movies.sort_values(
            by='score', ascending=False
        ).sample(frac=1, random_state=42).reset_index(drop=True)

        top_movies = recommended_movies.head(n_recommendations)

        return [
            {
                'movieId': row.get('movieId', None),
                'title': row['title'],
                'genres': row['genres'],
                'score': row['score'],
                'source': row.get('source', 'IMDb')
            }
            for _, row in top_movies.iterrows()
        ]

    def get_popular_movies(self, n_recommendations=10, industry="All"):
        """Get top-rated movies based on 'score'."""
        movies_to_consider = self._filter_by_industry(self.movies_df, industry)
        if movies_to_consider.empty:
            print(f"⚠️ No movies for industry '{industry}'. Returning empty list.")
            return []

        popular_movies = movies_to_consider.sort_values(
            by='score', ascending=False
        ).head(n_recommendations)

        return [
            {
                'movieId': row.get('movieId', None),
                'title': row['title'],
                'genres': row['genres'],
                'score': row['score'],
                'source': row.get('source', 'IMDb')
            }
            for _, row in popular_movies.iterrows()
        ]
