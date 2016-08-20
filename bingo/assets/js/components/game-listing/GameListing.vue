<template>
  <div class="lst-Items">
    <div class="lst-Item" v-for="game in current_games">
      <a href="{{ game.id }}/"><h1>{{ game.id }}</h1></a>
      <p>Game {{ pending(game.start_time) ? 'starts' : 'started' }} {{ game.start_time | fromNow }}</p>
    </div>
  </div>
</template>

<script type="text/ecmascript-6">
import moment from 'moment'

export default {
  data () {
    return {
      current_games: [],
      socket: null
    }
  },

  ready () {
    // When we're using HTTPS, use WSS too.
    const scheme = window.location.protocol === 'https:' ? 'wss' : 'ws'
    this.socket = new WebSocket(`${scheme}://${window.location.host.replace(':3', ':8')}/games/`)
    this.socket.onmessage = this.handleSocketOnMessage
    this.socket.onopen = this.handleSocketOnOpen
  },

  methods: {
    handleSocketOnMessage (e) {
      this.current_games = JSON.parse(e.data).current_games
    },
    handleSocketOnOpen (e) {
      this.socket.send(JSON.stringify({
        'text': 'REQUEST_GAMES'
      }))
    },
    pending (time) {
      return moment() < moment(time)
    }
  },

  filters: {
    fromNow: function (date) {
      return moment(date).fromNow();
    }
  }
}
</script>
