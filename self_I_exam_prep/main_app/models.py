from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models

from main_app.custom_managers import HouseManager


# Create your models here.
class House(models.Model):
    name = models.CharField(
        max_length=80,
        validators=[
            MinLengthValidator(5)
        ],
        unique=True
    )
    motto = models.TextField(
        blank=True,
        null=True
    )
    is_ruling = models.BooleanField(
        default=False
    )
    castle = models.CharField(
        max_length=80,
        blank=True,
        null=True
    )
    wins = models.PositiveSmallIntegerField(
        default=0
    )
    modified_at = models.DateTimeField(
        auto_now=True
    )

    objects = HouseManager()

class Dragon(models.Model):
    class DefinedBreath(models.TextChoices):
        FIRE = 'Fire', 'Fire'
        ICE = 'Ice', 'Ice'
        LIGHTNING = 'Lightning', 'Lightning'
        UNKNOWN = 'Unknown', 'Unknown'


    name = models.CharField(
        max_length=80,
        validators=[
            MinLengthValidator(5)
        ],
        unique=True
    )
    power = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
        default=1
    )
    breath = models.CharField(
        max_length=9,
        choices=DefinedBreath.choices,
        default='Unknown'
    )
    is_healthy = models.BooleanField(
        default=False
    )
    birth_date = models.DateField(
        auto_now_add=True
    )
    wins = models.PositiveSmallIntegerField(
        default=0
    )
    modified_at = models.DateTimeField(
        auto_now=True
    )
    house = models.ForeignKey(
        'House',
        on_delete=models.CASCADE,
        related_name='dragons'
    )

class Quest(models.Model):
    name = models.CharField(
        max_length=80,
        validators=[
            MinLengthValidator(5)
        ],
        unique=True
    )
    code = models.CharField(
        max_length=4,
        validators=[
            RegexValidator(r'^[A-Za-z#]{4}$')
        ],
        unique=True
    )
    reward = models.FloatField(
        default=100.0
    )
    start_time = models.DateTimeField()
    modified_at = models.DateTimeField(
        auto_now=True
    )
    dragons = models.ManyToManyField(
        'Dragon',
        related_name='quests'
    )
    host = models.ForeignKey(
        'House',
        on_delete=models.CASCADE,
        related_name='quests'
    )