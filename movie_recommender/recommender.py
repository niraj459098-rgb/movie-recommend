"""
recommender.py
Implements three classic recommendation techniques:
  1. Content-Based Filtering   - TF-IDF over genres + cosine similarity
  2. Collaborative Filtering   - Item-based, cosine similarity over the user-item rating matrix
  3. Matrix Factorization      - Truncated SVD (latent factors) over the user-item matrix
"""
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD


class MovieRecommender:
    def __init__(self, movies_path="data/movies.csv", ratings_path="data/ratings.csv"):
        self.movies = pd.read_csv(movies_path)
        self.ratings = pd.read_csv(ratings_path)
        self._build_content_model()
        self._build_user_item_matrix()
        self._build_collaborative_model()
        self._build_svd_model()

    # ---------------------------------------------------------------
    # 1. CONTENT-BASED FILTERING
    # ---------------------------------------------------------------
    def _build_content_model(self):
        genre_text = self.movies["genres"].str.replace("|", " ", regex=False)
        self.tfidf = TfidfVectorizer(token_pattern=r"[A-Za-z0-9\-]+")
        tfidf_matrix = self.tfidf.fit_transform(genre_text)
        self.content_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        self.title_to_idx = pd.Series(self.movies.index, index=self.movies["title"]).to_dict()

    def recommend_content_based(self, title, top_n=8):
        if title not in self.title_to_idx:
            return {"error": f"Movie '{title}' not found."}
        idx = self.title_to_idx[title]
        sim_scores = list(enumerate(self.content_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = [s for s in sim_scores if s[0] != idx][:top_n]
        return self._format_results(sim_scores)

    # ---------------------------------------------------------------
    # Shared: build user-item ratings matrix
    # ---------------------------------------------------------------
    def _build_user_item_matrix(self):
        self.user_item = self.ratings.pivot_table(
            index="userId", columns="movieId", values="rating"
        ).fillna(0)
        self.movie_ids = self.user_item.columns.tolist()
        self.movie_id_to_col = {m: i for i, m in enumerate(self.movie_ids)}

    # ---------------------------------------------------------------
    # 2. COLLABORATIVE FILTERING (item-based, cosine similarity)
    # ---------------------------------------------------------------
    def _build_collaborative_model(self):
        item_matrix = self.user_item.T.values  # rows = movies, cols = users
        self.item_sim = cosine_similarity(item_matrix)

    def recommend_collaborative(self, user_id, top_n=8):
        if user_id not in self.user_item.index:
            return {"error": f"User {user_id} not found."}
        user_ratings = self.user_item.loc[user_id].values
        rated_mask = user_ratings > 0
        if rated_mask.sum() == 0:
            return {"error": "User has no ratings yet."}

        # Predicted score for every movie = weighted avg of similar, rated movies
        scores = self.item_sim.dot(user_ratings) / (
            np.abs(self.item_sim).sum(axis=1) + 1e-9
        )
        scores[rated_mask] = -np.inf  # exclude already-rated movies
        top_idx = np.argsort(scores)[::-1][:top_n]
        results = []
        for i in top_idx:
            if scores[i] == -np.inf:
                continue
            movie_id = self.movie_ids[i]
            row = self.movies[self.movies.movieId == movie_id].iloc[0]
            results.append({
                "movieId": int(movie_id),
                "title": row.title,
                "genres": row.genres,
                "score": round(float(scores[i]), 3),
            })
        return results

    # ---------------------------------------------------------------
    # 3. MATRIX FACTORIZATION (Truncated SVD / latent factors)
    # ---------------------------------------------------------------
    def _build_svd_model(self, n_factors=15):
        matrix = self.user_item.values
        n_factors = min(n_factors, min(matrix.shape) - 1)
        self.svd = TruncatedSVD(n_components=n_factors, random_state=42)
        self.user_factors = self.svd.fit_transform(matrix)
        self.item_factors = self.svd.components_
        self.reconstructed = np.dot(self.user_factors, self.item_factors)

    def recommend_svd(self, user_id, top_n=8):
        if user_id not in self.user_item.index:
            return {"error": f"User {user_id} not found."}
        row_pos = self.user_item.index.get_loc(user_id)
        predicted = self.reconstructed[row_pos]
        actual = self.user_item.loc[user_id].values
        predicted = predicted.copy()
        predicted[actual > 0] = -np.inf  # exclude already-rated
        top_idx = np.argsort(predicted)[::-1][:top_n]
        results = []
        for i in top_idx:
            if predicted[i] == -np.inf:
                continue
            movie_id = self.movie_ids[i]
            row = self.movies[self.movies.movieId == movie_id].iloc[0]
            results.append({
                "movieId": int(movie_id),
                "title": row.title,
                "genres": row.genres,
                "score": round(float(predicted[i]), 3),
            })
        return results

    # ---------------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------------
    def _format_results(self, sim_scores):
        results = []
        for idx, score in sim_scores:
            row = self.movies.iloc[idx]
            results.append({
                "movieId": int(row.movieId),
                "title": row.title,
                "genres": row.genres,
                "score": round(float(score), 3),
            })
        return results

    def all_movies(self):
        return self.movies.to_dict(orient="records")

    def all_user_ids(self):
        return sorted(self.user_item.index.tolist())

    def user_rated_movies(self, user_id):
        if user_id not in self.user_item.index:
            return []
        ratings_row = self.user_item.loc[user_id]
        rated = ratings_row[ratings_row > 0].sort_values(ascending=False)
        out = []
        for movie_id, rating in rated.items():
            row = self.movies[self.movies.movieId == movie_id].iloc[0]
            out.append({"movieId": int(movie_id), "title": row.title, "rating": float(rating)})
        return out
