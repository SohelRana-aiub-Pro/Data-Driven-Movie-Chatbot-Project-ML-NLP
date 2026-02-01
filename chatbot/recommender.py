import os
import requests
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA_DIR = "data"
BASICS_URL = "https://datasets.imdbws.com/title.basics.tsv.gz"
RATINGS_URL = "https://datasets.imdbws.com/title.ratings.tsv.gz"

def download_imdb_data():
    """Download IMDb datasets automatically if not present."""
    os.makedirs(DATA_DIR, exist_ok=True)

    basics_path = os.path.join(DATA_DIR, "title.basics.tsv.gz")
    ratings_path = os.path.join(DATA_DIR, "title.ratings.tsv.gz")

    if not os.path.exists(basics_path):
        print("Downloading title.basics.tsv.gz...")
        r = requests.get(BASICS_URL, stream=True)
        with open(basics_path, "wb") as f:
            f.write(r.content)

    if not os.path.exists(ratings_path):
        print("Downloading title.ratings.tsv.gz...")
        r = requests.get(RATINGS_URL, stream=True)
        with open(ratings_path, "wb") as f:
            f.write(r.content)

    return basics_path, ratings_path

def load_movies():
    """Load and merge IMDb basics + ratings."""
    basics_path, ratings_path = download_imdb_data()

    basics = pd.read_csv(basics_path, sep="\t", na_values="\\N", compression="gzip")
    ratings = pd.read_csv(ratings_path, sep="\t", na_values="\\N", compression="gzip")

    movies_df = basics.merge(ratings, on="tconst", how="inner")
    movies_df = movies_df[movies_df["titleType"] == "movie"]
    movies_df["genres"] = movies_df["genres"].fillna("Unknown")

    return movies_df

movies_df = load_movies()

def recommend_movies(query: str, limit: int = 5):
    """Recommend movies based on user query (title or genre)."""
    movies_df["combined"] = movies_df["primaryTitle"].astype(str) + " " + movies_df["genres"].astype(str)

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(movies_df["combined"])

    query_vec = vectorizer.transform([query])
    similarity = cosine_similarity(query_vec, tfidf_matrix).flatten()

    indices = similarity.argsort()[::-1][:limit]
    recommendations = movies_df.iloc[indices]


    return recommendations.to_dict(orient="records")