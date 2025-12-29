# 🎬 Movie & TV Show Recommendation App

A content-based recommendation system built using **Python**, **Streamlit**, and **scikit-learn**. This app recommends similar Movies and TV Shows based on textual features (plot, genre, keywords) and provides "Top Charts" for specific genres.

It fetches real-time posters and plot summaries using the **OMDb API**.

![Demo Screenshot](https://github.com/user-attachments/assets/c900ab70-3837-4d98-8a2a-897e3c1cdeed)

---

## 🚀 Demo

[Live App](https://movie-recommendation-8u90.onrender.com/) ---

## 📌 Features

- **Dual Mode:** Switch seamlessly between **Movies** and **TV Shows**.
- **Two Search Methods:**
    - **By Similarity:** Find content similar to your favorite title (using Cosine Similarity).
    - **By Genre:** Browse top-rated content for specific genres (e.g., "Comedy", "Sci-Fi").
- **Live Data:** Fetches official posters and plot summaries via the **OMDb API**.
- **Smart Filtering:** Automatically filters non-English content and removes duplicates.
- **Optimized Performance:** Uses pre-computed similarity matrices to handle large datasets efficiently.

---

## 📁 Project Structure

```bash
movie-recommendation-app/
│
├── src/
│   ├── main.py                # Main Streamlit app (UI)
│   ├── preprocess.py          # Script to clean data & generate models
│   ├── recommend.py           # Logic for similarity & genre filtering
│   ├── omdb_utils.py          # Helper to fetch posters from OMDb API
│   ├── movies.csv             # Raw Movie Dataset
│   ├── tv_shows.csv           # Raw TV Show Dataset
│   ├── *.pkl                  # Generated models (ignored by Git)
│
├── requirements.txt           # Dependencies
└── README.md                  # This file

```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone [https://github.com/yourusername/movie-recommendation-app.git](https://github.com/yourusername/movie-recommendation-app.git)
cd movie-recommendation-app/src

```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

```

### 3. Install Dependencies

```bash
pip install -r ../requirements.txt

```

### 4. Get an API Key

Get a free API key from [OMDb API](http://www.omdbapi.com/apikey.aspx). You will need this to see posters.

---

## ▶️ Setup & Run

### Step 1: Generate the Models

Before running the app, you must process the raw CSV files to create the similarity matrices.

```bash
python preprocess.py

```

*This will create `.pkl` files in your directory. You only need to run this once.*

### Step 2: Run the App

You can run the app by providing your API key in the command line:

**Windows (PowerShell):**

```powershell
$env:OMDB_API_KEY="your_api_key_here"
streamlit run main.py

```

**Mac / Linux:**

```bash
OMDB_API_KEY="your_api_key_here" streamlit run main.py

```

*Alternatively, create a `.streamlit/secrets.toml` file containing `OMDB_API_KEY = "your_key"`.*

---

## 🧠 How It Works

1. **Preprocessing:**
* The app ingests `movies.csv` and `tv_shows.csv`.
* It cleans the text (removing stopwords) and combines metadata (Genres + Keywords + Taglines).
* It converts text into numbers using **TF-IDF Vectorization**.
* It calculates the **Cosine Similarity** between every item to find matches.


2. **Recommendation Engine:**
* **Similarity Search:** Looks up the pre-calculated similarity scores to find the closest matches to your input.
* **Genre Search:** Filters the dataset for the selected genre and sorts results by **popularity**.



---

## 📊 Dataset

This project uses data compatible with the **TMDB (The Movie Database)** format:

* **Movies:** ~5,000 top rated movies.
* **TV Shows:** ~5,000 top rated TV shows.

*Note: Raw CSV files are included, but `.pkl` files are generated locally to save space.*

---

## 📦 Requirements

* `streamlit`
* `pandas`
* `scikit-learn`
* `nltk`
* `requests`

---

## 📝 License

This project is open source and available under the [MIT License](https://www.google.com/search?q=LICENSE).

