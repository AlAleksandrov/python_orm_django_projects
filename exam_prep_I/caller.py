import os
import django
from django.db.models import Q, Count, Avg, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from orm_skeleton.helpers import populate_model_with_data
from main_app.models import Director, Actor, Movie

# Create queries within functions

def populate_db() -> None:
    # populate_model_with_data(Director)
    # populate_model_with_data(Actor)
    # populate_model_with_data(Movie)

    director1 = Director.objects.create(
        full_name='John Lennon',
        birth_date='1968-10-11',
        nationality='British',
        years_of_experience=10
    )
    director2 = Director.objects.create(
        full_name='larry Banana',
        birth_date='1973-01-21',
        nationality='British',
        years_of_experience=5
    )

    actor1 = Actor.objects.create(
        full_name='John Snow',
        birth_date='1978-12-01',
        nationality='British',
        is_awarded=True,
        last_updated='2022-03-12 12:00:00'
    )
    actor2 = Actor.objects.create(
        full_name='Jorge Santorini',
        birth_date='1965-06-15',
        nationality='Italian',
        is_awarded=False,
        last_updated='2024-07-25 12:00:00'
    )

    movie1 = Movie.objects.create(
        title='The Shawshank Redemption',
        release_date='1994-10-14',
        storyline='Prisoners and fight to free a woman who has been beaten up by her father.',
        genre='DRAMA',
        rating=9.2,
        is_classic=True,
        director=director1,
        starring_actor=actor1,
    )
    movie2 = Movie.objects.create(
        title='The Shark',
        release_date='2014-03-24',
        storyline='A shark attacks a prisoners family.',
        genre='ACTION',
        rating=8.7,
        is_classic=False,
        director=director2,
        starring_actor=actor2,
    )

# populate_db()

def get_directors(search_name=None, search_nationality=None) -> str | None:
    if search_name is None and search_nationality is None:
        return ''

    query_name = Q(full_name__icontains=search_name)
    query_nationality = Q(nationality__icontains=search_nationality)

    if search_name is not None and search_nationality is not None:
        query = Q(query_name & query_nationality)
    elif search_name is not None:
        query = query_name
    else:
        query = query_nationality

    directors = Director.objects.filter(query).order_by('full_name')

    if not directors:
        return ''

    return '\n'.join(f'Director: {d.full_name}, nationality: {d.nationality}, experience: {d.years_of_experience}' for d in directors)

def get_top_director() -> str:
    # top_director = Director.objects.get_directors_by_movies_count().first()
    top_director = Director.objects.annotate(
        movies_count=Count('director_movies')
    ).order_by(
        '-movies_count',
        'full_name',
    ).first()

    if not top_director:
        return ''

    return f'Top director: {top_director.full_name}, movies: {top_director.movies_count}.'

def get_top_actor() -> str:
    top_actor = Actor.objects.prefetch_related(
        'actor_movies'
    ).annotate(
        movies_count=Count('actor_movies'),
        avg_rating=Avg('actor_movies__rating')
    ).order_by(
        '-movies_count',
        'full_name',
    ).first()

    if not top_actor or top_actor.movies_count:
        return ''

    movies = ', '.join(m.title for m in top_actor.starring_movies.all() if m)

    return f"Top Actor: {top_actor.full_name}, starring in movies: {movies}, movies average rating: {top_actor.avg_rating:.1f}"


def get_actors_by_movies_count() -> str:
    actors = Actor.objects.annotate(
        movies_count=Count('actor_movies')
    ).order_by(
        '-movies_count',
        'full_name',
    )[:3]

    if not actors or not actors[0].movies_count:
        return ''

    return '\n'.join(f'{a.full_name}, participated in {a.movies_count} movies' for a in actors)

def get_top_rated_awarded_movie() -> str:
    top_movie = Movie.objects.select_related(
        'starring_actor'
    ).prefetch_related(
        'actors'
    ).filter(
        is_awarded=True
    ).order_by(
        '-rating',
        'title'
    ).first()

    if not top_movie:
        return ''

    starring_actor = top_movie.starring_actor.full_name if top_movie.starring_actor else 'N/A'
    participating_actors = ', '.join(top_movie.actors.order_by('full_name').values_list('full_name', flat=True))

    return f'Top rated awarded movie: {top_movie.title}, rating: {top_movie.rating:.1f}. Starring actor: {starring_actor}. Cast: {participating_actors}.'

def increase_rating() -> str:
    movies_to_update = Movie.objects.filter(is_classic=True, rating__lt=10)

    if not movies_to_update:
        return 'No ratings increased.'

    movies_to_update.update(rating=F('rating') + 0.1)

    return f'Rating increased for {movies_to_update.count()} movies.'