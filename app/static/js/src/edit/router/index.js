import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

import EditChoices from '../components/EditChoices.vue'
import DeleteItem from '../components/DeleteItem.vue'

import Opponent from '../components/opponent/Details.vue'
import OpponentList from '../components/opponent/List.vue'
import OpponentAdd from '../components/opponent/Add.vue'
import OpponentEdit from '../components/opponent/Edit.vue'

import Competition from '../components/competition/Details.vue'
import CompetitionList from '../components/competition/List.vue'
import CompetitionAdd from '../components/competition/Add.vue'
import CompetitionEdit from '../components/competition/Edit.vue'


export default new VueRouter({routes:[
  { path: '/', component: EditChoices},

  { path: '/opponent-list', component: OpponentList},
  { path: '/add-opponent', component: OpponentAdd},
  { path: '/opponent/:opponent_id/delete', component: DeleteItem, name: 'opponent-delete', props: true},
  { path: '/opponent/:opponent_id', component: Opponent, name: 'opponent', props: true},
  { path: '/opponent/:opponent_id/edit', component: OpponentEdit, name: 'opponent-edit', props: true},

  { path: '/competition-list', component: CompetitionList},
  { path: '/add-competition', component: CompetitionAdd},
  { path: '/competition/:competition_id/delete', component: DeleteItem, name: 'competition-delete', props: true},
  { path: '/competition/:competition_id', component: Competition, name: 'competition', props: true},
  { path: '/competition/:competition_id/edit', component: CompetitionEdit, name: 'competition-edit', props: true}

]
});