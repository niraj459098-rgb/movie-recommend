"""
Generates a small MovieLens-style dataset (movies.csv + ratings.csv)
so the recommender system has real data to work with.
"""
import csv
import random

random.seed(42)

MOVIES = [
    (1, "The Shawshank Redemption", "Drama"),
    (2, "The Godfather", "Crime|Drama"),
    (3, "The Dark Knight", "Action|Crime|Drama"),
    (4, "Pulp Fiction", "Crime|Drama"),
    (5, "Forrest Gump", "Drama|Romance"),
    (6, "Inception", "Action|Sci-Fi|Thriller"),
    (7, "The Matrix", "Action|Sci-Fi"),
    (8, "Interstellar", "Adventure|Drama|Sci-Fi"),
    (9, "Fight Club", "Drama|Thriller"),
    (10, "Goodfellas", "Crime|Drama"),
    (11, "The Lord of the Rings: The Fellowship of the Ring", "Adventure|Fantasy"),
    (12, "Se7en", "Crime|Thriller"),
    (13, "The Silence of the Lambs", "Crime|Thriller"),
    (14, "Saving Private Ryan", "Drama|War"),
    (15, "The Green Mile", "Crime|Drama|Fantasy"),
    (16, "Gladiator", "Action|Adventure|Drama"),
    (17, "The Prestige", "Drama|Mystery|Sci-Fi"),
    (18, "The Departed", "Crime|Drama|Thriller"),
    (19, "Whiplash", "Drama|Music"),
    (20, "The Lion King", "Animation|Adventure|Drama"),
    (21, "Toy Story", "Animation|Adventure|Comedy"),
    (22, "Finding Nemo", "Animation|Adventure|Comedy"),
    (23, "Up", "Animation|Adventure|Comedy"),
    (24, "Coco", "Animation|Adventure|Family"),
    (25, "Shrek", "Animation|Adventure|Comedy"),
    (26, "Avengers: Endgame", "Action|Adventure|Sci-Fi"),
    (27, "Iron Man", "Action|Adventure|Sci-Fi"),
    (28, "Guardians of the Galaxy", "Action|Adventure|Comedy"),
    (29, "Spider-Man: Into the Spider-Verse", "Animation|Action|Adventure"),
    (30, "Black Panther", "Action|Adventure|Sci-Fi"),
    (31, "Titanic", "Drama|Romance"),
    (32, "The Notebook", "Drama|Romance"),
    (33, "La La Land", "Comedy|Drama|Music"),
    (34, "Pretty Woman", "Comedy|Romance"),
    (35, "500 Days of Summer", "Comedy|Drama|Romance"),
    (36, "Get Out", "Horror|Mystery|Thriller"),
    (37, "A Quiet Place", "Horror|Sci-Fi|Thriller"),
    (38, "The Conjuring", "Horror|Mystery|Thriller"),
    (39, "It", "Horror|Fantasy"),
    (40, "Hereditary", "Horror|Mystery|Drama"),
    (41, "3 Idiots", "Comedy|Drama"),
    (42, "Dangal", "Action|Biography|Drama"),
    (43, "PK", "Comedy|Drama|Sci-Fi"),
    (44, "Zindagi Na Milegi Dobara", "Comedy|Drama"),
    (45, "Queen", "Comedy|Drama"),
    (46, "Dilwale Dulhania Le Jayenge", "Drama|Romance"),
    (47, "Andhadhun", "Crime|Thriller|Comedy"),
    (48, "Baahubali: The Beginning", "Action|Drama|Fantasy"),
    (49, "Taare Zameen Par", "Drama|Family"),
    (50, "Lagaan", "Adventure|Drama|Sport"),
]

NUM_USERS = 200
MIN_RATINGS, MAX_RATINGS = 8, 25

def generate_ratings():
    rows = []
    genre_bias_pool = ["Drama", "Action", "Comedy", "Sci-Fi", "Romance",
                        "Thriller", "Animation", "Horror", "Crime", "Adventure"]
    for user_id in range(1, NUM_USERS + 1):
        fav_genres = random.sample(genre_bias_pool, k=random.randint(2, 3))
        n_ratings = random.randint(MIN_RATINGS, MAX_RATINGS)
        movie_pool = list(MOVIES)
        random.shuffle(movie_pool)

        def score(movie):
            genres = movie[2].split("|")
            return sum(1 for g in genres if g in fav_genres)

        movie_pool.sort(key=score, reverse=True)
        chosen = movie_pool[:n_ratings]
        random.shuffle(chosen)

        for movie in chosen:
            base = 3.0 + score(movie) * 0.8
            rating = max(1.0, min(5.0, round(base + random.uniform(-1.2, 1.2) * 2) / 2))
            rows.append((user_id, movie[0], rating))
    return rows


def main():
    with open("data/movies.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["movieId", "title", "genres"])
        writer.writerows(MOVIES)

    ratings = generate_ratings()
    with open("data/ratings.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["userId", "movieId", "rating"])
        writer.writerows(ratings)

    print(f"Generated {len(MOVIES)} movies and {len(ratings)} ratings for {NUM_USERS} users.")


if __name__ == "__main__":
    main()
