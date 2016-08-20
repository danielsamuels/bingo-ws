<template>
  <!-- Numbers called -->
  <table class="dtl-Called">
    <tr v-for="row in available_numbers">
      <td align="center" v-for="number in row">
        {{ number.value }}
      </td>
    </tr>
  </table>

  <!-- Player cards -->
  <h1>Your cards</h1>

  <table v-for="card in player_cards" style="margin-bottom: 15px;">
    <tr>
      <td style="border: 1px solid #000; text-align: center; font-weight: bold;">{{ card[0][0] }}</td>
      <td style="border: 1px solid #000; text-align: center; font-weight: bold;">{{ card[1][0] }}</td>
      <td style="border: 1px solid #000; text-align: center; font-weight: bold;">{{ card[2][0] }}</td>
      <td style="border: 1px solid #000; text-align: center; font-weight: bold;">{{ card[3][0] }}</td>
      <td style="border: 1px solid #000; text-align: center; font-weight: bold;">{{ card[4][0] }}</td>
      <td style="border: 1px solid #000; text-align: center; font-weight: bold;">{{ card[5][0] }}</td>
      <td style="border: 1px solid #000; text-align: center; font-weight: bold;">{{ card[6][0] }}</td>
      <td style="border: 1px solid #000; text-align: center; font-weight: bold;">{{ card[7][0] }}</td>
      <td style="border: 1px solid #000; text-align: center; font-weight: bold;">{{ card[8][0] }}</td>
    </tr>
    <tr>
      <td style="border: 1px solid #000; text-align: center; font-weight: bold;">{{ card[0][1] }}</td>
      <td style="border: 1px solid #000; text-align: center; font-weight: bold;">{{ card[1][1] }}</td>
      <td style="border: 1px solid #000; text-align: center; font-weight: bold;">{{ card[2][1] }}</td>
      <td style="border: 1px solid #000; text-align: center; font-weight: bold;">{{ card[3][1] }}</td>
      <td style="border: 1px solid #000; text-align: center; font-weight: bold;">{{ card[4][1] }}</td>
      <td style="border: 1px solid #000; text-align: center; font-weight: bold;">{{ card[5][1] }}</td>
      <td style="border: 1px solid #000; text-align: center; font-weight: bold;">{{ card[6][1] }}</td>
      <td style="border: 1px solid #000; text-align: center; font-weight: bold;">{{ card[7][1] }}</td>
      <td style="border: 1px solid #000; text-align: center; font-weight: bold;">{{ card[8][1] }}</td>
    </tr>
    <tr>
      <td style="border: 1px solid #000; text-align: center; font-weight: bold;">{{ card[0][2] }}</td>
      <td style="border: 1px solid #000; text-align: center; font-weight: bold;">{{ card[1][2] }}</td>
      <td style="border: 1px solid #000; text-align: center; font-weight: bold;">{{ card[2][2] }}</td>
      <td style="border: 1px solid #000; text-align: center; font-weight: bold;">{{ card[3][2] }}</td>
      <td style="border: 1px solid #000; text-align: center; font-weight: bold;">{{ card[4][2] }}</td>
      <td style="border: 1px solid #000; text-align: center; font-weight: bold;">{{ card[5][2] }}</td>
      <td style="border: 1px solid #000; text-align: center; font-weight: bold;">{{ card[6][2] }}</td>
      <td style="border: 1px solid #000; text-align: center; font-weight: bold;">{{ card[7][2] }}</td>
      <td style="border: 1px solid #000; text-align: center; font-weight: bold;">{{ card[8][2] }}</td>
    </tr>
  </table>

  9x3
</template>

<script type="text/ecmascript-6">
import moment from 'moment'

Array.prototype.randomElement = function () {
  var desiredIndex = Math.floor(Math.random() * this.length)
  return this.splice(desiredIndex, 1)[0]
}

export default {
  data () {
    return {
      numbersCalled: {},
      numCards: 6,
      socket: null,
    }
  },

  ready () {
    // When we're using HTTPS, use WSS too.
    const scheme = window.location.protocol === 'https:' ? 'wss' : 'ws'
    this.socket = new WebSocket(`${scheme}://${window.location.host.replace(':3', ':8')}/games${window.location.pathname}`)
    this.socket.onmessage = this.handleSocketOnMessage
    this.socket.onopen = this.handleSocketOnOpen
  },

  computed: {
    available_numbers () {
      let number_rows = []
      let numbers = []

      for (let i = 1; i <= 90; i++) {
        numbers.push({
          'value': i,
          'called': false
        })

        if (numbers.length === 10) {
          number_rows.push(numbers)
          numbers = []
        }
      }

      return number_rows
    },

    player_cards () {
      let cards = [
        [
          [], [], [], [], [], [], [], [], []
        ],
        [
          [], [], [], [], [], [], [], [], []
        ],
        [
          [], [], [], [], [], [], [], [], []
        ],
        [
          [], [], [], [], [], [], [], [], []
        ],
        [
          [], [], [], [], [], [], [], [], []
        ],
        [
          [], [], [], [], [], [], [], [], []
        ],
      ]

      for (let column = 1; column <= 9; column++) {
        // Column 1 => 01 - 10
        // Column 2 => 11 - 20
        // Column 3 => 21 - 30
        // ...

        // Split each group of 10 numbers across the 6 cards.
        let baseValue = ((column - 1) * 10) + 1
        let availableNumbers = this.range(baseValue, baseValue + 9)

        // Grab a random value from the list of available numbers.
        while (availableNumbers.length > 0) {
          let value = availableNumbers.randomElement()

          // Add this value to the a random card.
          // cards.forEach((card) => {
          //   if (value === null) {
          //     return
          //   }

          //   if (card[column - 1].length < 3) {
          //     card[column - 1].push(value)
          //     value = null
          //   }
          // })
        }
      }
      return cards
    }
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
    },

    range (start, end) {
      return [...Array(end - start + 1)].map((_, i) => start + i)
    }
  },

  filters: {
    fromNow: function (date) {
      return moment(date).fromNow();
    }
  }
}
</script>
