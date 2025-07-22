# omdb_api.py
import requests
import os
from dotenv import load_dotenv

class OMDbAPI:
    def __init__(self, api_key=None):
        load_dotenv() # Load environment variables from .env file
        self.api_key = api_key or os.getenv('OMDB_API_KEY')
        self.base_url = "http://www.omdbapi.com/"
    
    def search_movie(self, title):
        """Search for a movie by title"""
        if not self.api_key:
            print("Error: OMDb API key is missing.")
            return None
        
        params = {
            'apikey': self.api_key,
            't': title
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('Response') == 'True':
                    return data  # Full movie data
                else:
                    # print(f"No results found for '{title}'.") # Suppress this for cleaner output
                    return None
            else:
                print(f"OMDb API error: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def get_movie_poster(self, title):
        """Get movie poster URL"""
        movie_data = self.search_movie(title)
        if movie_data and movie_data.get('Poster') and movie_data['Poster'] != 'N/A':
            return movie_data['Poster']
        return "https://via.placeholder.com/500x750?text=No+Image"
    
    def get_movie_details(self, title):
        """Get detailed movie information"""
        movie_data = self.search_movie(title)
        if movie_data:
            return {
                'title': movie_data.get('Title', title),
                'overview': movie_data.get('Plot', 'No description available.'),
                'release_date': movie_data.get('Released', 'Unknown'),
                'rating': movie_data.get('imdbRating', 'N/A'),
                'poster_url': self.get_movie_poster(title)
            }
        return None
