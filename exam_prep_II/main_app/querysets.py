from django.db import models
from django.db.models import QuerySet
from django.db.models.aggregates import Count


class ProfileQuerySet(models.QuerySet):
    def get_regular_customers(self) -> QuerySet:
        return self.annotate(
            count_orders=Count('order')
        ). filter(
            count_orders__gt=2,
        ).order_by(
            '-count_orders'
        )