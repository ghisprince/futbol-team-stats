import '@babel/polyfill'
import Vue from 'vue'

import './plugins/vuetify'
import App from './App.vue'
import router from './router'
import store from './store'
require('../src/assets/fonts.googleapis.roboto.css')
Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
