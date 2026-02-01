from chatbot.recommender import recommend_movies


def handle_user_query(query: str):
    """Process user query and return chatbot response."""
    movies = recommend_movies(query)
    responses = []
    for m in movies:
        responses.append(
            f"🎬 {m['primaryTitle']} ({m['startYear']})\n"
            f"Genre: {m['genres']}\n"
            f"IMDb Rating: {m['averageRating']}"
        )
    return responses