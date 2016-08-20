<template>
  <!-- Numbers called -->
  <div class="dtl-Columns">
    <div class="dtl-Column dtl-Column-called">
      <div class="dtl-LastCalled_Outer" v-if="!pending(startTime)">
        <div class="dtl-LastCalled_Title">Last called:</div>
        <div class="dtl-LastCalled_Value">{{ lastCalled }}</div>
      </div>

      <div class="dtl-TimeToStart_Outer" v-if="pending(startTime)">
        {{ startTime | fromNow }}
      </div>

      <table class="dtl-Called">
        <tr v-for="row in available_numbers">
          <td align="center" v-for="number in row" class="dlt-Called_Cell" :class="{
            'dlt-Called_Cell-called': numbersCalledNumeric.indexOf(number.value) !== -1
          }">
            {{ number.value }}
          </td>
        </tr>
      </table>
    </div>

    <div class="dtl-Column">
      <!-- Player cards -->
      <div class="gm-Cards_Outer">
        <h1 class="gm-Cards_Title">Your cards</h1>

        <div class="gm-Cards_Items">
          <table class="gm-Cards_Item" style="">
            <tr v-for="row in 18">
              <td v-for="column in 9" class="gm-Cards_TableCell">
                <!-- For this column, take the slice and see if this row is in there -->
                <!-- {{ column * 10 }}, {{ (column + 1) * 10 }}<br> -->
                <!-- {{ playerCards.slice(column * 10, (column + 1) * 10) }} -->
                <span v-if="playerCards.slice(column * 10, (column + 1) * 10).indexOf(row) !== -1">x</span>

                <!--
                <input v-if="card[column][row] !== emptyValue" type="checkbox" id="{{ index }}-{{ row }}-{{ column }}" class="gm-Cards_Checkbox">
                <label v-if="card[column][row] !== emptyValue" for="{{ index }}-{{ row }}-{{ column }}" class="gm-Cards_Label">{{ card[column][row] }}</label>
                -->
              </td>
            </tr>
          </table>
        </div>
      </div>
    </div>
  </template>

<script type="text/ecmascript-6">
import moment from 'moment'

Array.prototype.randomElement = function () {
  const desiredIndex = Math.floor(Math.random() * this.length)
  return this[desiredIndex]
}

Array.prototype.removeRandomElement = function () {
  const desiredIndex = Math.floor(Math.random() * this.length)
  return this.splice(desiredIndex, 1)[0]
}

Array.prototype.randomInsert = function (item) {
  const desiredIndex = Math.floor(Math.random() * this.length)
  this.splice(desiredIndex, 0, item);
};

Math.seed = function(s) {
    return function() {
        s = Math.sin(s) * 10000;
        return s - Math.floor(s);
    };
};

Math.random = Math.seed(1);

export default {
  data () {
    return {
      numbersCalled: [],
      numCards: 6,
      socket: null,
      startTime: null,
      emptyValue: '-----',
      speechEnabled: false,
      bingoLingo: {
        1: "Number One, Kelly's Eye",
        2: "One Little Duck, Number Two",
        3: "Three, a Cup of Tea",
        4: "Number four, Knock at the Door",
        5: "Number five, Man Alive",
        6: "Number 6, Tom Mix",
        7: "Lucky 7, woohoo",
        8: "8, Garden Gate",
        9: "Number 9, Doctors Orders",
        10: "Number 10, Theresa's Den",
        11: "11, Legs Eleven",
        12: "One Dozen, 12",
        13: "13, Unlucky for Some",
        14: "Valentines Day, number 14",
        15: "15, Young and Keen",
        16: "Sweet Sixteen",
        17: "17, Dancing Queen",
        18: "Coming of Age, 18",
        19: "19, Goodbye-Teens",
        20: "20, One Score",
        21: "21, Key in the Door",
        22: "Two Little Ducks, 22",
        23: "23, Thee and Me",
        24: "Two Dozen, 24",
        25: "Duck and Dive, 25",
        26: "26, Pick and Mix",
        27: "Gateway to Heaven, 27",
        28: "28, Over Weight",
        29: "29, Rise and Shine",
        30: "number 30, Dirty Gertie ",
        31: "Get up and Run, number 31",
        32: "Buckle my Shoe, 32",
        33: "33, Dirty Knee",
        34: "34, Ask for More",
        35: "Jump and Jive, 35",
        36: "36, Three Dozen",
        37: "More than Eleven, 37",
        38: "38, Christmas Cake",
        39: "39, Steps",
        40: "Naughty Forty",
        41: "41, Time for Fun",
        42: "42, Winnie the Pooh",
        43: "43, Down on your Knees",
        44: "44, Droopy Drawers",
        45: "45, Halfway There",
        46: "46, Up to Tricks",
        47: "Four and Seven, 47",
        48: "48, Four Dozen,",
        49: "49, PC",
        50: "Half a Century, 50",
        51: "Tweak of the Thumb, 51",
        52: "52, Danny La Rue",
        53: "Stuck in the Tree, 53",
        54: "Clean the Floor, 54",
        55: "55, Snakes Alive",
        56: "Was she worth it, 56",
        57: "57, Heinz Varieties",
        58: "58, Make them Wait",
        59: "59, Brighton Line",
        60: "60: Five Dozen",
        61: "61, Bakers Bun",
        62: "62, Turn in the Screw",
        63: "Tickle Me 63",
        64: "Red Raw, 64",
        65: "Old Age Pension, 65",
        66: "Clickety Click, 66",
        67: "Made in Heaven, 67",
        68: "Saving Grace, 68",
        69: "Either Way Up, 69",
        70: "Three Score & Ten, 70",
        71: "Bang on the Drum, 71",
        72: "Six Dozen, 72",
        73: "Queen B, 73",
        74: "Candy Store, 74",
        75: "Strive & Strive, 75",
        76: "76, Trombones",
        77: "77, Sunset Strip",
        78: "78, Heavens Gate",
        79: "One More Time, 79",
        80: "Eight & Blank, 80",
        81: "Stop & Run, 81",
        82: "Straight On Through, 82",
        83: "Time for Tea, 83",
        84: "84, Seven Dozen",
        85: "85, Staying Alive",
        86: "Between the Sticks, 86",
        87: "Torquay in Devon, 87",
        88: "Two Fat Ladies, 88",
        89: "Nearly There, 89",
        90: "Top of the Shop, number 90",
      }
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

    lastCalled () {
      if (this.numbersCalled.length === 0) {
        return 'Waiting..'
      }

      return this.numbersCalled[this.numbersCalled.length - 1].value
    },

    numbersCalledNumeric () {
      let numbers = []

      this.numbersCalled.forEach((item) => {
        numbers.push(item.value)
      })

      return numbers
    },

    playerCards () {
      console.log('player_cards')

      let cards = [
        [[], [], [], [], [], [], [], [], []],
        [[], [], [], [], [], [], [], [], []],
        [[], [], [], [], [], [], [], [], []],
        [[], [], [], [], [], [], [], [], []],
        [[], [], [], [], [], [], [], [], []],
        [[], [], [], [], [], [], [], [], []],
      ]

      // For each column, figure out which rows are going to get values.
      // At this point we don't care what the values _are_, just whether
      // a row should have one or not.
      //
      // For the first five columns, it's easy -- all rows are eligible, so
      // just choose 10 of the 18.  After that, we need to remove rows which
      // have already been selected 5 times.

      let allChosenRows = []
      let chosenRowCounter = {}

      for (let column = 1; column <= 9; column++) {
        let chosenRows = []

        // Choose our 10 rows for this column.
        for (let i = 1; i <= 10; i++) {
          let availableRows = this.range(0, 17)

          // Are there any values which appear 5 times in allChosenRows?
          const fullRows = Object.keys(chosenRowCounter).filter((element) => chosenRowCounter[element] >= 5)

          if (fullRows.length > 0) {
            availableRows = availableRows.filter((element) => fullRows.indexOf(element.toString()) === -1)
          }

          // Remove any rows which have already been selected for this column.
          availableRows = availableRows.filter((element) => chosenRows.indexOf(element) === -1)

          const chosenRow = availableRows.removeRandomElement()
          chosenRows.push(chosenRow)

          if (chosenRowCounter[chosenRow] === undefined) {
            chosenRowCounter[chosenRow] = 1
          } else {
            chosenRowCounter[chosenRow]++
          }
        }

        allChosenRows.push(...chosenRows)
      }

      // We may have some rows with less than 5 items.
      // We may have some card columns which are empty.

      // Now we need to populate the cards with the marks.
      console.log(allChosenRows)
      console.log(allChosenRows.length)
      return allChosenRows
    },

    player_cards2 () {
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

        // Add spaces randomly.
        for (let r = 1; r < 9; r++) {
          availableNumbers.randomInsert(this.emptyValue)
        }

        while (availableNumbers.length > 0) {
          // Grab the first value from the list of available numbers.
          let value = availableNumbers.shift()

          // Group the cards by the number of values (non-blank) in their column.
          let smallestValue = 3
          let smallestCards = []

          cards.forEach((card, index) => {
            if (card[column - 1].length >= 3) {
              return
            }

            let trueLength = card[column - 1].filter(Number).length

            if (value === this.emptyValue && trueLength === 0 && card[column - 1].length === 2) {
              return
            }

            // If we were to insert an item into this column, which row would it fall into?
            const prospectiveRow = card[column - 1].length

            // Are there already 5 items in this row?
            let rowItems = 0

            card.forEach((cardColumn) => {
              if (cardColumn.filter(Number).length < prospectiveRow + 1) {
                return
              }

              if (cardColumn[prospectiveRow] !== this.emptyValue) {
                rowItems++
              }
            })

            if (rowItems >= 5) {
              return
            }

            if (trueLength < smallestValue) {
              smallestValue = trueLength
              smallestCards = [index]
            } else if (trueLength === smallestValue) {
              smallestCards.push(index)
            }
          })

          // Add to a random card.
          const randEl = smallestCards.randomElement()

          if (randEl === undefined) {
            // We need to look again..
            console.error(`Nowhere to put ${value}`)
          } else {
            console.log(`randEl: ${randEl}, smallestCards: ${smallestCards}`)
            cards[randEl][column - 1].push(value)
          }
        }
      }

      return cards
    }
  },

  methods: {
    handleSocketOnMessage (e) {
      // Based on the message type, we want to do different things.
      const data = JSON.parse(e.data)

      if (data.type === 'CONNECT') {
        // Populate the inital data.
        this.startTime = data.start_time
        this.numbersCalled = data.numbers_called

      } else if (data.type === 'NUMBER_DRAWN') {
        this.numbersCalled.push(data.number)

        if (this.speechEnabled) {
          var msg = new SpeechSynthesisUtterance(this.bingoLingo[data.number.value]);
          window.speechSynthesis.speak(msg);
        }
      }

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
