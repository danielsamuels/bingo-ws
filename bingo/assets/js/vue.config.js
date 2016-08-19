import Vue from 'vue'

import components from './components'

import store from './store'

Vue.filter('toString', (val) => {
  return String(val)
})

Vue.config.debug = true

export default {
  components,
  store,

  vuex: {
    getters: {},

    actions: {}
  },

  events: {
    overflowBody (val) {
      if (val) {
        document.body.style.overflow = 'hidden'
      } else {
        document.body.style.overflow = ''
      }
    }
  }
}
