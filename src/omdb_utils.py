# omdb_utils.py
import requests

def get_movie_details(title, api_key, media_type="movie"):
    """
    Fetches Plot and Poster from OMDb API.
    
    Args:
        title (str): The title of the content.
        api_key (str): Your OMDb API key.
        media_type (str): 'movie' or 'series' (important for accuracy).
        
    Returns:
        tuple: (plot, poster_url)
    """
    if not title or not api_key:
        return "N/A", "N/A"

    # cleaning title slightly to ensure better matching
    clean_title = title.strip()
    
    # URL construction with 'type' parameter
    url = f"http://www.omdbapi.com/?t={clean_title}&apikey={api_key}&type={media_type}&plot=short"

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("Response") == "True":
            plot = data.get("Plot", "Plot not available.")
            poster = data.get("Poster", "N/A")
            return plot, poster
        else:
            return "N/A", "N/A"
            
    except Exception as e:
        print(f"Error fetching details for {title}: {e}")
        return "Error", "N/A"