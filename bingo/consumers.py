from channels.generic.websockets import JsonWebsocketConsumer


class GameListingConsumer(JsonWebsocketConsumer):

    channel_session = True

    def connection_groups(self, **kwargs):
        return ['game-listing']

    def connect(self, message, **kwargs):
        self.send({
            'current_games': [
                '44802c50-9d24-417f-95f9-5cd8ea0db551'
            ]
        })


class GameDetailConsumer(JsonWebsocketConsumer):

    channel_session = True

    def connection_groups(self, **kwargs):
        return ['game-detail-{}'.format(kwargs['room'])]

    def connect(self, message, **kwargs):
        # Send game details: numbers already picked, time started etc.
        self.send({
            'current_numbers': {
                'value': '66',
                'order': '1',
                'timestamp': '2016-08-01T17:34:00+01:00'
            }
        })
