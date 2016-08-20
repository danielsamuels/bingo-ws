from channels.routing import route_class

from .apps.games import consumers

channel_routing = [
    route_class(consumers.GameListingConsumer, path=r'^/games/$'),
    route_class(consumers.GameDetailConsumer, path=r'^/games/(?P<room>[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[ab89][a-f0-9]{3}-[a-f0-9]{12})/$'),
]
