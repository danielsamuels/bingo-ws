<template>
  <div class="lst-Items">
    <div class="lst-Item" v-for="game in current_games">
      {{ game.id }}
      {{ game.start_time }}
    </div>
  </div>
</template>

<script type="text/ecmascript-6">
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
    }
  }
}
</script>
