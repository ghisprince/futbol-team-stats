import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)


import Opponent from '../components/Opponents.vue'
import OpponentList from '../components/OpponentsList.vue'
import OpponentAdd from '../components/OpponentsAdd.vue'
import OpponentEdit from '../components/OpponentsEdit.vue'
import OpponentDelete from '../components/OpponentsDelete.vue'


export default new VueRouter({routes:[
  { path: '/', component: OpponentList},
  { path: '/opponent/:opponent_id', component: Opponent, name: 'opponent'},
  { path: '/add-opponent', component: OpponentAdd},
  { path: '/opponent/:opponent_id/edit', component: OpponentEdit, name: 'opponent-edit'},
  { path: '/opponent/:opponent_id/delete', component: OpponentDelete, name: 'opponent-delete'}
]});