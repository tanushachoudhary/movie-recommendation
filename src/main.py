# main.py
import streamlit as st
import os
# Updated imports to match the new recommend.py
from recommend import df_movies, df_tv, recommend_movies, recommend_tv_shows
from omdb_utils import get_movie_details # Ensure this function handles the 'type' param as discussed before

# --- API Key Setup ---
OMDB_API_KEY = os.environ.get("OMDB_API_KEY")

# 2. If not found, try getting it from Streamlit Secrets (safely)
if not OMDB_API_KEY:
    try:
        OMDB_API_KEY = st.secrets["OMDB_API_KEY"]
    except Exception:
        # This block catches the error if secrets.toml doesn't exist
        pass

# 3. If still not found, stop the app
if not OMDB_API_KEY:
    st.error("❌ OMDB_API_KEY not found. Please set it in environment variables or create a .streamlit/secrets.toml file.")
    st.stop()

st.set_page_config(page_title="PopcornPick", page_icon="🎬", layout="centered")

st.title("🎬 PopcornPick - Movies and Shows Recommendations")

# --- 1. Toggle between Movies and TV Shows ---
category = st.radio("What are you looking for?", ["Movies", "TV Shows"], horizontal=True)

if category == "Movies":
    if df_movies is None:
        st.error("Movies data missing! Run 'python preprocess.py' first.")
        st.stop()
    
    # Setup for Movies
    content_list = sorted(df_movies['title'].dropna().unique())
    recommend_func = recommend_movies
    api_type = "movie"
    
else:
    if df_tv is None:
        st.error("TV data missing! Run 'python preprocess.py' first.")
        st.stop()
        
    # Setup for TV
    content_list = sorted(df_tv['title'].dropna().unique())
    recommend_func = recommend_tv_shows
    api_type = "series"

# --- 2. Dropdown and Button ---
selected_content = st.selectbox(f"Select a {category[:-1]}:", content_list)

if st.button(f"🚀 Recommend {category}"):
    with st.spinner(f"Finding similar {category}..."):
        recommendations = recommend_func(selected_content)
        
        if recommendations is None or recommendations.empty:
            st.warning("Sorry, no recommendations found.")
        else:
            st.success(f"Top similar {category}:")
            
            for _, row in recommendations.iterrows():
                title = row['title']
                
                # Dynamic media_type based on your earlier selection
                # If category is "Movies", use "movie", else "series"
                current_media_type = "movie" if category == "Movies" else "series"
                
                # Call the API
                plot, poster = get_movie_details(title, OMDB_API_KEY, media_type=current_media_type)

                with st.container():
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if poster != "N/A":
                            st.image(poster, width=120)
                        else:
                            # Fallback if no poster exists
                            st.image("https://via.placeholder.com/150x225?text=No+Poster", width=120)
                    with col2:
                        st.markdown(f"### {title}")
                        st.write(plot)
                    st.divider()