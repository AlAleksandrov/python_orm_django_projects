from django.db import models
from django.db.models import Count


class PublisherManager(models.Manager):
    def get_publishers_by_books_count(self):
        return self.annotate(
            books_count=Count('books')
        ).order_by(
            '-books_count',
            'name'
        )