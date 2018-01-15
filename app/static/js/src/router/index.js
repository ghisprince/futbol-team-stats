import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

import DeleteItem from '../components/DeleteItem.vue'

import Opponent from '../components/opponent/Details.vue'
import OpponentList from '../components/opponent/List.vue'
import OpponentAdd from '../components/opponent/Add.vue'
import OpponentEdit from '../components/opponent/Edit.vue'

import Competition from '../components/competition/Details.vue'
import CompetitionList from '../components/competition/List.vue'
import CompetitionAdd from '../components/competition/Add.vue'
import CompetitionEdit from '../components/competition/Edit.vue'

import Player from '../components/player/Details.vue'
import PlayerList from '../components/player/List.vue'
import PlayerAdd from '../components/player/Add.vue'
import PlayerEdit from '../components/player/Edit.vue'

import Match from '../components/match/Details.vue'
import MatchList from '../components/match/List.vue'
import MatchAdd from '../components/match/Add.vue'
import MatchEdit from '../components/match/Edit.vue'
import PlayerMatchEdit from '../components/player_match/Edit.vue'
import PlayerMatchAdd from '../components/player_match/Add.vue'

export default new VueRouter({routes:[
  { path: '/opponent-list', component: OpponentList},
  { path: '/add-opponent', component: OpponentAdd},
  { path: '/opponent/:opponent_id/delete', component: DeleteItem, name: 'opponent-delete', props: true},
  { path: '/opponent/:opponent_id', component: Opponent, name: 'opponent'},
  { path: '/opponent/:opponent_id/edit', component: OpponentEdit, name: 'opponent-edit'},

  { path: '/competition-list', component: CompetitionList},
  { path: '/add-competition', component: CompetitionAdd},
  { path: '/competition/:competition_id/delete', component: DeleteItem, name: 'competition-delete', props: true},
  { path: '/competition/:competition_id', component: Competition, name: 'competition'},
  { path: '/competition/:competition_id/edit', component: CompetitionEdit, name: 'competition-edit'},

  { path: '/player-list', component: PlayerList},
  { path: '/add-player', component: PlayerAdd},
  { path: '/player/:player_id/delete', component: DeleteItem, name: 'player-delete', props: true},
  { path: '/player/:player_id', component: Player, name: 'player'},
  { path: '/player/:player_id/edit', component: PlayerEdit, name: 'player-edit'},

  { path: '/match-list', component: MatchList},
  { path: '/add-match', component: MatchAdd},
  { path: '/match/:match_id/delete', component: DeleteItem, name: 'match-delete', props: true},
  { path: '/match/:match_id', component: Match, name: 'match'},
  { path: '/match/:match_id/edit', component: MatchEdit, name: 'match-edit'},
  { path: '/playermatch/:playermatch_id/edit', component: PlayerMatchEdit, name: 'playermatch-edit'},
  { path: '/playermatch/:match_id/add', component: PlayerMatchAdd, name: 'playermatch-add'}


]
});