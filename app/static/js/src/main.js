import Vue from 'vue'
import App from './App.vue'
import router from './router/index.js'
import moment from 'moment'
import Spinner from 'vue-simple-spinner'


new Vue({
  el: '#app-container',
  router,
  components: {
    Spinner
  },
  render: h => h(App)
})

Vue.filter('formatDate', function(value) {
  if (value) {
    return moment.utc(String(value)).format('YYYY/MM/DD hh:mm a')
  }
})