from channels.generic.websockets import JsonWebsocketConsumer
from django.utils.timezone import now
from .apps.games.models import Game
from datetime import timedelta

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
        # Send game details: numbers already picked, time started etc.
        self.send({
            'current_numbers': {
                'value': '66',
                'order': '1',
                'timestamp': '2016-08-01T17:34:00+01:00'
            }
        })
