# 🎬 Movie Recommendation App

A simple content-based movie recommendation system built using **Python**, **Streamlit**, and **scikit-learn**. This app recommends similar movies based on your input using cosine similarity over textual features.

---

## 🚀 Demo

[Live App on Streamlit](https://your-deployed-url.streamlit.app/) <!-- Replace with actual URL once deployed -->

---

## 📌 Features

- Search for any movie from the dataset
- Get top 5 similar movie recommendations
- Clean, minimal UI built with **Streamlit**
- Uses **TF-IDF Vectorization** and **Cosine Similarity** under the hood

---

## 📁 Project Structure

```

movie-recommendation-app/
│
├── app.py                 # Main Streamlit app
├── movies.csv             # Dataset containing movie info
├── requirements.txt       # Dependencies
└── README.md              # This file

````

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/movie-recommendation-app.git
cd movie-recommendation-app
````

### 2. Create a Virtual Environment (optional but recommended)

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the App Locally

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🧠 How It Works

* Movie descriptions (or metadata) are vectorized using **TF-IDF**
* The app computes **cosine similarity** between movie vectors
* Based on your selected movie, the app recommends top similar movies

---

## 📊 Dataset

This project uses a simplified movie dataset with columns like:

* `title`: Movie title
* `overview`: Description used for similarity comparison

---

## 📦 Requirements

See `requirements.txt`, but mainly:

* `streamlit`
* `pandas`
* `scikit-learn`
* `numpy`


---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).
