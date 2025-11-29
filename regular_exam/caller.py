import os
from decimal import Decimal

import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Publisher, Author, Book
from orm_skeleton.helpers import populate_model_with_data
from django.db.models import Q, Count, Avg, F, Value


# Create queries within functions
def populate_db() -> None:
    populate_model_with_data(Publisher)
    populate_model_with_data(Author)
    populate_model_with_data(Book)

def get_publishers(search_string=None) -> str:
    if search_string is None:
        return "No search criteria."

    publishers = Publisher.objects.filter(
        Q(name__icontains=search_string)
            |
        Q(country__icontains=search_string)
    ).order_by(
        '-rating',
        'name'
    )

    if not publishers.exists():
        return "No publishers found."

    return '\n'.join(
        f'Publisher: {p.name}, '
        f'country: {p.country if p.country != "TBC" else "Unknown"}, '
        f'rating: {p.rating:.1f}' for p in publishers
    )

def get_top_publisher() -> str:
    publisher = Publisher.objects.get_publishers_by_books_count().first()

    if publisher:
        return f"Top Publisher: {publisher.name} with {publisher.books_count} books."

    return "No publishers found."


def get_top_main_author() -> str:
    main_author = Author.objects.annotate(
        books_count=Count('main_books'),
        books_avg_rating=Avg('main_books__rating')
    ).filter(
        books_count__gt=0
    ).order_by(
        '-books_count',
        'name'
    ).first()

    if not main_author:
        return "No results."

    book_titles_lst = main_author.main_books.order_by('title').values_list('title', flat=True)
    book_titles = ', '.join(book_titles_lst)


    return (f"Top Author: {main_author.name}, "
            f"own book titles: {book_titles}, "
            f"books average rating: {main_author.books_avg_rating:.1f}")


def get_authors_by_books_count() -> str:
    authors = Author.objects.annotate(
        num_books=Count('main_books', distinct=True) + Count('co_books', distinct=True)
    ).filter(
        num_books__gt=0
    ).order_by(
        '-num_books',
        'name'
    )[:3]

    if not authors:
        return "No results."

    return '\n'.join(f'{a.name} authored {a.num_books} books.' for a in authors)

def get_bestseller() -> str:
    books = Book.objects.filter(
        is_bestseller=True
    ).annotate(
        co_authors_count=Count('co_authors', distinct=True),
        authors_count=F('co_authors_count') + Value(1),
        composite_index=F('rating') + (F('co_authors_count') + Value(1))
    ).order_by(
        '-composite_index',
        '-rating',
        '-authors_count',
        'title'
    )

    if not books.exists():
        return "No results."

    bestseller = books.first()

    main_author_name = bestseller.main_author.name
    co_author_names = '/'.join(
        bestseller.co_authors.order_by('name').values_list('name', flat=True)
    )

    return (f"Top bestseller: {bestseller.title}, "
            f"index: {bestseller.composite_index:.1f}. "
            f"Main author: {main_author_name}. "
            f"Co-authors: {co_author_names if co_author_names else 'N/A'}.")

def increase_price() -> str:
    books = Book.objects.annotate(
        total_rating=F('rating') + F('publisher__rating')
    ).filter(
        publication_date__year=2025,
        total_rating__gte=8.0
    )

    if not books.exists():
        return "No changes in price."

    expensive_books = books.filter(price__gt=Decimal('50.00'))
    cheap_books = books.filter(price__lte=Decimal('50.00'))

    if expensive_books.exists():
        expensive_books.update(price=F('price') * Decimal('1.10'))

    if cheap_books.exists():
        cheap_books.update(price=F('price') * Decimal('1.20'))

    return f"Prices increased for {expensive_books.count() + cheap_books.count()} book/s."