# recommend.py
import joblib
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# --- Load Data ---
try:
    df_movies = joblib.load('movies_df.pkl')
    sim_movies = joblib.load('movies_sim.pkl')
    logging.info("✅ Movies data loaded.")
except FileNotFoundError:
    df_movies, sim_movies = None, None

try:
    df_tv = joblib.load('tv_df.pkl')
    sim_tv = joblib.load('tv_sim.pkl')
    logging.info("✅ TV data loaded.")
except FileNotFoundError:
    df_tv, sim_tv = None, None

def get_recommendations(title, df, cosine_sim, top_n=10):
    """
    Standard recommendation based on similarity (cosine_sim).
    Explicitly filters out the input 'title' from results.
    """
    if df is None or cosine_sim is None:
        return None

    # 1. Find the index of the selected title
    idx_list = df[df['title'].str.lower() == title.lower()].index
    if len(idx_list) == 0:
        return None
    idx = idx_list[0]

    # 2. Get similarity scores
    scores = list(enumerate(cosine_sim[idx]))
    
    # 3. Sort by score (descending)
    # We take top_n + 5 just in case we need to remove duplicates/self
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[:top_n+5]
    
    # 4. Retrieve candidate rows
    movie_indices = [i[0] for i in scores]
    candidates = df.iloc[movie_indices][['title']].copy()

    # --- CRITICAL FIX: Remove the selected movie itself ---
    # We filter out any row where the title matches the input title
    candidates = candidates[candidates['title'].str.lower() != title.lower()]

    # 5. Return strictly the requested amount (top_n)
    return candidates.head(top_n).reset_index(drop=True)

def get_recommendations_by_genre(genre, df, top_n=10):
    """
    Returns top popular items for a specific genre string.
    """
    if df is None: return None
    
    mask = df['genres'].str.contains(genre, case=False, na=False)
    filtered_df = df[mask]
    
    result = filtered_df.sort_values(by='popularity', ascending=False).head(top_n)
    return result[['title']].reset_index(drop=True)

def get_unique_genres(df):
    if df is None: return []
    unique_genres = set()
    for genres_str in df['genres'].dropna():
        parts = [g.strip() for g in genres_str.split(',')]
        unique_genres.update(parts)
    return sorted(list(unique_genres))

# Wrappers
def recommend_movies(title):
    return get_recommendations(title, df_movies, sim_movies)

def recommend_tv_shows(title):
    return get_recommendations(title, df_tv, sim_tv)