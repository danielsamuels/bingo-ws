import uuid

from django.db import models
from django.core import validators


class Game(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    start_time = models.DateTimeField()

    end_time = models.DateTimeField(
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['-start_time']


class Number(models.Model):

    game = models.ForeignKey(Game)

    value = models.PositiveIntegerField(
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(90),
        ]
    )

    call_order = models.PositiveIntegerField(
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(90),
        ]
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ['call_order']
