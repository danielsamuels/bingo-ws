from channels import Group
from channels.auth import channel_session


# Connected to websocket.connect
@channel_session
def game_listing_connect(message):
    print 'START game_listing_connect'

    # Add them to the right group
    print 'adding to group'
    Group('game-listing').add(message.reply_channel)

    # Let them know what the current list of games are.
    print 'sending current games'
    message.reply_channel.send({
        'current_games': [
            '44802c50-9d24-417f-95f9-5cd8ea0db551'
        ]
    })

    Group('game-listing').send({
        'current_games': [
            '44802c50-9d24-417f-95f9-5cd8ea0db552'
        ]
    })

    print 'END game_listing_connect'
    print ''


# Connected to websocket.receive
@channel_session
def game_listing_message(message):
    print 'START game_listing_message'

    print message.content
    print message['text']

    message.reply_channel.send({'text': 'PONG'})
    print 'sent reply back', message.reply_channel

    Group('game-listing').send({
        "text": 'testing..',
    })

    print 'END game_listing_message'
    print ''


# Connected to websocket.disconnect
@channel_session
def game_listing_disconnect(message):
    print 'game_listing_disconnect'

    Group('game-listing').discard(message.reply_channel)


# Connected to websocket.connect
@channel_session
def game_detail_connect(message):
    print 'game_detail_connect'

    # Add them to the right group
    Group('game-').add(message.reply_channel)


# Connected to websocket.receive
@channel_session
def game_detail_message(message):
    print 'game_detail_message'

    Group('game-').send({
        "text": message['text'],
    })


# Connected to websocket.disconnect
@channel_session
def game_detail_disconnect(message):
    print 'game_detail_disconnect'

    Group('game-').discard(message.reply_channel)
