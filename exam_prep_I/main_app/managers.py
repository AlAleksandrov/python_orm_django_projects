from django.db import models


class DirectorManager(models.Manager):
    def get_directors_by_movies_count(self):
        return self.annotate(
            movies_count=models.Count(
                'director_movies'
            )
        ).order_by('-movies_count', 'full_name')