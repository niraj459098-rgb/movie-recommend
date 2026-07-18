# CineMatch — Movie Recommendation System

A mini project (AI/ML, Python) implementing a movie recommender with a
Flask backend and an interactive web frontend. Built for a B.Tech CSE
mini project submission.

## Techniques implemented

| Technique | File | Idea |
|---|---|---|
| **Content-Based Filtering** | `recommender.py` → `recommend_content_based` | Represents each movie's genres as a TF-IDF vector and ranks other movies by cosine similarity to the selected movie. |
| **Collaborative Filtering** | `recommender.py` → `recommend_collaborative` | Item-based CF: builds a user–item rating matrix, computes cosine similarity between movies based on how users rated them, then scores unseen movies as a similarity-weighted average of the user's past ratings. |
| **Matrix Factorization** | `recommender.py` → `recommend_svd` | Uses Truncated SVD to factor the user–item matrix into latent "taste factor" matrices, reconstructs predicted ratings, and recommends the highest predicted, not-yet-rated movies. |

## Project structure

```
movie_recommender/
├── app.py               # Flask app + REST API routes
├── recommender.py        # All three recommendation engines
├── generate_data.py       # Builds the synthetic MovieLens-style dataset
├── data/
│   ├── movies.csv        # 50 movies with genres
│   └── ratings.csv        # ~3,200 simulated ratings from 200 users
├── templates/
│   └── index.html         # Frontend page
├── static/
│   ├── style.css           # Cinema-themed styling
│   └── script.js            # Frontend logic (fetch calls to the API)
└── requirements.txt
```

## How to run

```bash
pip install -r requirements.txt
python generate_data.py     # (already generated once, re-run to regenerate)
python app.py
```

Then open **http://localhost:5000** in your browser.

## API endpoints

- `GET /api/movies` — list of all movies
- `GET /api/users` — list of all user IDs
- `GET /api/user/<id>/ratings` — a user's rating history
- `GET /api/recommend/content?title=<movie title>` — content-based recs
- `GET /api/recommend/collaborative?user_id=<id>` — collaborative filtering recs
- `GET /api/recommend/svd?user_id=<id>` — matrix factorization recs

## Dataset note

Real MovieLens data requires an internet download, so this project ships
with a self-contained, synthetically generated dataset (50 well-known
movies, 200 simulated user profiles with genre-biased rating patterns) that
mimics the structure of MovieLens (`movieId, title, genres` /
`userId, movieId, rating`). You can swap in real MovieLens CSVs by
replacing the files in `data/` — the schema is identical, so no code
changes are needed.

## For your presentation

A matching PowerPoint deck (`CineMatch_Presentation.pptx`) is included,
covering: problem statement, techniques, system architecture, tech stack,
demo screenshots, results/evaluation and future scope.
