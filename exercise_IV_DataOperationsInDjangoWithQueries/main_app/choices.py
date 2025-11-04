from django.db import models


class RoomTypeChoice(models.TextChoices):
    STANDARD = 'Standard', 'Standard'
    DELUXE = 'Deluxe', 'Deluxe'
    SUITE = 'Suite','Suite'