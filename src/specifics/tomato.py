from rottentomatoes import Movie

def retrieveMovie(movie_title: str) -> Movie | None:
    print(movie_title)
    try:
        movie = Movie(movie_title=movie_title)
        return movie
    except LookupError:
        return None