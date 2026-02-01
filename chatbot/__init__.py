# Marks this folder as a Python package
# Optional: expose key functions for cleaner imports
from .logic import handle_user_query
from .recommender import recommend_movies
from .utils import format_response

__all__ = ["handle_user_query", "recommend_movies", "format_response"]