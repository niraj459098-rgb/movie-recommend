"""
app.py - Flask backend for the Movie Recommendation System.
Serves the frontend and exposes REST API endpoints for all three
recommendation techniques.
"""
from flask import Flask, jsonify, render_template, request
from recommender import MovieRecommender

app = Flask(__name__)
engine = MovieRecommender()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/movies")
def api_movies():
    return jsonify(engine.all_movies())


@app.route("/api/users")
def api_users():
    return jsonify(engine.all_user_ids())


@app.route("/api/user/<int:user_id>/ratings")
def api_user_ratings(user_id):
    return jsonify(engine.user_rated_movies(user_id))


@app.route("/api/recommend/content")
def api_content():
    title = request.args.get("title", "")
    top_n = int(request.args.get("top_n", 8))
    return jsonify(engine.recommend_content_based(title, top_n))


@app.route("/api/recommend/collaborative")
def api_collaborative():
    user_id = int(request.args.get("user_id", 1))
    top_n = int(request.args.get("top_n", 8))
    return jsonify(engine.recommend_collaborative(user_id, top_n))


@app.route("/api/recommend/svd")
def api_svd():
    user_id = int(request.args.get("user_id", 1))
    top_n = int(request.args.get("top_n", 8))
    return jsonify(engine.recommend_svd(user_id, top_n))


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
