import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)


import Player from '../components/Players.vue'
import PlayerList from '../components/PlayersList.vue'
import PlayerAdd from '../components/PlayersAdd.vue'
import PlayerEdit from '../components/PlayersEdit.vue'
import PlayerDelete from '../components/PlayersDelete.vue'


export default new VueRouter({routes:[
  { path: '/', component: PlayerList},
  { path: '/player/:player_id', component: Player, name: 'player'},
  { path: '/add-player', component: PlayerAdd},
  { path: '/player/:player_id/edit', component: PlayerEdit, name: 'player-edit'},
  { path: '/player/:player_id/delete', component: PlayerDelete, name: 'player-delete'}
]});