import pandas as pd
import re
import nltk
import joblib
import logging
import os
import ast
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logging.info("🚀 Starting preprocessing...")

nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = str(text) 
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    return " ".join(tokens)

def parse_genres(x):
    """
    Extracts genre names from JSON strings (for movies) 
    or returns the string as-is (for TV shows).
    """
    if isinstance(x, str) and (x.startswith('[') or x.startswith('{')):
        try:
            # Safely evaluate string representation of list/dict
            genres_list = ast.literal_eval(x)
            if isinstance(genres_list, list):
                return ", ".join([g['name'] for g in genres_list])
        except:
            return x
    return str(x)

def train_recommender(csv_file, output_prefix, limit=10000):
    logging.info(f"📂 Processing file: {csv_file}")
    
    if not os.path.exists(csv_file):
        logging.error(f"❌ File not found: {csv_file}")
        return

    try:
        df = pd.read_csv(csv_file, engine='python', on_bad_lines='skip')
        
        # 1. Normalize Column Names
        if 'name' in df.columns:
            df.rename(columns={'name': 'title'}, inplace=True)
            
        # 2. Add/Clean Columns
        for col in ['genres', 'keywords', 'overview', 'tagline', 'popularity', 'original_language']:
            if col not in df.columns:
                df[col] = ''
            if col == 'popularity':
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # 3. Clean Genres (Convert JSON to "Action, Comedy")
        df['genres'] = df['genres'].apply(parse_genres)

        # 4. Filter English Only
        if 'original_language' in df.columns:
            df = df[df['original_language'] == 'en']

        # 5. Sort by Popularity and Limit
        # (This is CRITICAL: Since many shows have identical genres, 
        # sorting by popularity ensures the best ones appear first)
        logging.info(f"📉 Reducing dataset to top {limit} popular items...")
        df = df.sort_values(by='popularity', ascending=False).head(limit)
        df = df.dropna(subset=['title']).reset_index(drop=True)

        # 6. Prepare Text for Vectorization
        # --- CHANGE HERE: WE ONLY USE GENRES NOW ---
        df['combined_text'] = df['genres'].fillna('').astype(str)
        
        df['cleaned_text'] = df['combined_text'].apply(preprocess_text)

        # 7. Vectorization & Similarity
        logging.info("🔠 Vectorizing...")
        tfidf = TfidfVectorizer(max_features=5000)
        tfidf_matrix = tfidf.fit_transform(df['cleaned_text'])

        logging.info("📐 Calculating cosine similarity...")
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

        # 8. Save Files 
        df_export = df[['title', 'genres', 'popularity']].copy()
        
        joblib.dump(df_export, f'{output_prefix}_df.pkl')
        joblib.dump(cosine_sim, f'{output_prefix}_sim.pkl')
        
        logging.info(f"✅ Success! Saved {output_prefix} files.")

    except Exception as e:
        logging.error(f"❌ Error: {e}")

if __name__ == "__main__":
    # Keeping your limit of 9000
    train_recommender("movies.csv", "movies", limit=9000)
    train_recommender("tv_shows.csv", "tv", limit=9000)