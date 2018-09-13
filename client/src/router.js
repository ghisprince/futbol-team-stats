import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/views/Home.vue'

import Competitions from '@/components/Competitions.vue'
import Competition from '@/components/Competition.vue'
import CompetitionCreate from '@/components/CompetitionCreate.vue'
import CompetitionEdit from '@/components/CompetitionEdit.vue'

import Opponents from '@/components/Opponents.vue'
import Opponent from '@/components/Opponent.vue'
import OpponentCreate from '@/components/OpponentCreate.vue'
import OpponentEdit from '@/components/OpponentEdit.vue'

import Match from '@/components/Match.vue'
import MatchEdit from '@/components/MatchEdit.vue'
import MatchCreate from '@/components/MatchCreate.vue'
import MatchStatsEdit from '@/components/MatchStatsEdit.vue'
import PlayerMatchEdit from '@/components/PlayerMatchEdit.vue'

import Players from '@/components/Players.vue'
import Player from '@/components/Player.vue'
import PlayerCreate from '@/components/PlayerCreate.vue'
import PlayerEdit from '@/components/PlayerEdit.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    // Competitions
    {
      path: '/competitions',
      name: 'Competitions',
      component: Competitions
    },
    {
      path: '/competitions/:id',
      name: 'Competition',
      component: Competition
    },
    {
      path: '/competitions/create',
      name: 'CompetitionCreate',
      component: CompetitionCreate
    },
    {
      path: '/competitions/:id/edit',
      name: 'CompetitionEdit',
      component: CompetitionEdit
    },
    // Opponents
    {
      path: '/opponents',
      name: 'Opponents',
      component: Opponents
    },
    {
      path: '/opponents/:id',
      name: 'Opponent',
      component: Opponent
    },
    {
      path: '/opponents/create',
      name: 'OpponentCreate',
      component: OpponentCreate
    },
    {
      path: '/opponents/:id/edit',
      name: 'OpponentEdit',
      component: OpponentEdit
    },

    // Matches
    {
      path: '/matches/:id',
      name: 'Match',
      component: Match
    },
    {
      path: '/matches/:id/edit',
      name: 'MatchEdit',
      component: MatchEdit
    },
    {
      path: '/matchs/create',
      name: 'MatchCreate',
      component: MatchCreate
    },
    // MatchStats
    {
      path: '/matchStats/:id/edit',
      name: 'MatchStatsEdit',
      component: MatchStatsEdit
    },
    
    {
      path: '/playerMatches/:id/edit',
      name: 'PlayerMatchEdit',
      component: PlayerMatchEdit
    },
    // Players
    {
      path: '/players',
      name: 'Players',
      component: Players
    },
    {
      path: '/players/:id',
      name: 'Player',
      component: Player
    },
    {
      path: '/players/create',
      name: 'PlayerCreate',
      component: PlayerCreate
    },
    {
      path: '/players/:id/edit',
      name: 'PlayerEdit',
      component: PlayerEdit
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/About.vue')
    }
  ]
})
