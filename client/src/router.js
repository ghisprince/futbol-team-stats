import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/views/Home.vue'
import store from '@/store'

import Competitions from '@/views/Competitions.vue'
import Competition from '@/views/Competition.vue'
import CompetitionCreate from '@/views/CompetitionCreate.vue'
import CompetitionEdit from '@/views/CompetitionEdit.vue'

import Seasons from '@/views/Seasons.vue'
import Season from '@/views/Season.vue'
import SeasonCreate from '@/views/SeasonCreate.vue'
import SeasonEdit from '@/views/SeasonEdit.vue'

import Opponents from '@/views/Opponents.vue'
import Opponent from '@/views/Opponent.vue'
import OpponentCreate from '@/views/OpponentCreate.vue'
import OpponentEdit from '@/views/OpponentEdit.vue'

import Match from '@/views/Match.vue'
import MatchEdit from '@/views/MatchEdit.vue'
import MatchCreate from '@/views/MatchCreate.vue'
import MatchStatsEdit from '@/views/MatchStatsEdit.vue'
import PlayerMatchEdit from '@/views/PlayerMatchEdit.vue'
import MatchShotsEdit from '@/views/MatchShotsEdit.vue'

import Players from '@/views/Players.vue'
import Player from '@/views/Player.vue'
import PlayerCreate from '@/views/PlayerCreate.vue'
import PlayerEdit from '@/views/PlayerEdit.vue'

import Login from '@/views/Login.vue'

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/login',
      name: 'logout',
      component: Login
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
    // Seasons
    {
      path: '/seasons',
      name: 'Seasons',
      component: Seasons
    },
    {
      path: '/seasons/:id',
      name: 'Season',
      component: Season
    },
    {
      path: '/seasons/create',
      name: 'SeasonCreate',
      component: SeasonCreate
    },
    {
      path: '/seasons/:id/edit',
      name: 'SeasonEdit',
      component: SeasonEdit
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
    {
      path: '/matchShotsEdit/:id/edit',
      name: 'MatchShotsEdit',
      component: MatchShotsEdit
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

router.beforeEach((to, from, next) => {
  if (from.name) {
    //  catch leaving PlayerGamesEdit and trigger refresh
    if (from.name === 'MatchShotsEdit') {
      store.dispatch('fetchOpponents')
      store.dispatch('fetchCompetitions')
      store.dispatch('fetchPlayers')
    }
  }
  next()
})

export default router
