from channels.routing import route

from .consumers import (game_detail_connect, game_detail_disconnect,
                        game_detail_message, game_listing_connect,
                        game_listing_disconnect, game_listing_message)

channel_routing = [
    # Game listing
    route("websocket.connect", game_listing_connect),
    route("websocket.receive", game_listing_message),
    route("websocket.disconnect", game_listing_disconnect),

    # Game detail
    # route("websocket.connect", game_detail_connect, path=r'^/games/(?P<room>[a-f0-9]{8}-?4[a-f0-9]{3}-?[a-f0-9]{4}-?[a-f0-9]{4}-?[a-f0-9]{12})/$'),
    # route("websocket.receive", game_detail_message, path=r'^/games/(?P<room>[a-f0-9]{8}-?4[a-f0-9]{3}-?[a-f0-9]{4}-?[a-f0-9]{4}-?[a-f0-9]{12})/$'),
    # route("websocket.disconnect", game_detail_disconnect, path=r'^/games/(?P<room>[a-f0-9]{8}-?4[a-f0-9]{3}-?[a-f0-9]{4}-?[a-f0-9]{4}-?[a-f0-9]{12})/$'),
]
