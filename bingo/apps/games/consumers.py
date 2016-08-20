import time
from datetime import timedelta

from channels.generic.websockets import JsonWebsocketConsumer
from django.db import IntegrityError
from django.utils.timezone import now

from .models import Game, Number

GAME_LISTING_CHANNEL = 'game-listing'
GAME_DETAIL_PREFIX = 'game-detail-'


def get_current_games():
    # Are there any games currently in the lobby?
    lobbies = Game.objects.filter(
        start_time__gte=now(),
    ).count()

    if not lobbies:
        # Create a new lobby.
        Game.objects.create(
            start_time=now() + timedelta(minutes=3)
        )

    # Expire any games which weren't played.
    Game.objects.filter(
        start_time__lte=now() - timedelta(minutes=60)
    ).update(
        end_time=now()
    )

    current_games = [
        {
            'id': str(game.id),
            'start_time': game.start_time.isoformat(),
        }
        for game in Game.objects.exclude(
            end_time__isnull=False,
        )
    ]

    return current_games


class GameListingConsumer(JsonWebsocketConsumer):

    channel_session = True

    def connection_groups(self, **kwargs):
        return [GAME_LISTING_CHANNEL]

    def connect(self, message, **kwargs):
        self.send({
            'current_games': get_current_games()
        })


class GameDetailConsumer(JsonWebsocketConsumer):

    channel_session = True

    def connection_groups(self, **kwargs):
        return [GAME_DETAIL_PREFIX + kwargs['room']]

    def connect(self, message, **kwargs):
        game = Game.objects.get(id=kwargs['room'])

        # Send game details: numbers already picked, time started etc.
        self.send({
            'type': 'CONNECT',
            'start_time': game.start_time.isoformat(),
            'numbers_called': game.numbers_called()
        })

        numbers_called = game.numbers_called()
        while len(numbers_called) < 90:
            time.sleep(10)

            self.group_send(
                GAME_DETAIL_PREFIX + kwargs['room'],
                {
                    'type': 'NUMBER_DRAWN',
                    'number': game.call_number()
                }
            )

            numbers_called = game.numbers_called()
