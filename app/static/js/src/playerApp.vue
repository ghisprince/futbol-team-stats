<template>
    <div id="app-style">

        <router-view></router-view>

    </div>
</template>

<script>



import Vue from 'vue';
import VueRouter from 'vue-router'
import Vuex from 'vuex'
import PlayerAdd from './components/PlayerAdd.vue'
import Player from './components/Player.vue'
import PlayerDelete from './components/PlayerDelete.vue'
import PlayerEdit from './components/PlayerEdit.vue'
import PlayerList from './components/PlayerList.vue'



var router = new VueRouter({routes:[
  { path: '/', component: PlayerList},
  { path: '/player/:player_id', component: Player, name: 'player'},
  { path: '/add-player', component: PlayerAdd},
  { path: '/player/:player_id/edit', component: PlayerEdit, name: 'player-edit'},
  { path: '/player/:player_id/delete', component: PlayerDelete, name: 'player-delete'}
]});

Vue.use(VueRouter)
Vue.use(Vuex)


export default {
    name: 'app',
    router,
    components: {},
    data () {
        return {}
    }
}

</script>

<style>
#app-style {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
}
</style>