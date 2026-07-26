from rottentomatoes import Movie

def retrieveMovie(movie_title: str) -> Movie | None:
    try:
        movie = Movie(movie_title=movie_title)
        return movie
    except LookupError:
        return None