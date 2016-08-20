import uuid
import random

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

    def numbers_called(self):
        return [number.serialize() for number in self.number_set.all()]

    def call_number(self):
        call_order = list(self.number_set.all())[-1].call_order + 1 if self.number_set.count() > 0 else 1
        random.seed(self.start_time.isoformat() + str(self.id) + str(call_order))

        choices = range(1, 91)

        # Remove any choices which have already been called.
        called = self.number_set.all().values_list('value', flat=True)

        valid_choices = [value for value in choices if value not in called]

        return Number.objects.create(
            game=self,
            value=random.choice(valid_choices),
            call_order=call_order
        ).serialize()

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

    def serialize(self):
        return {
            'value': self.value,
            'call_order': self.call_order,
            'timestamp': self.timestamp.isoformat(),
        }

    class Meta:
        ordering = ['call_order']
        unique_together = [['game', 'value']]
