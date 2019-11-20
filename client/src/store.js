import Vue from 'vue'
import Vuex from 'vuex'
import API from '@/lib/API'
import router from '@/router'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    team: { id: 1 },
    user:
      { username: '',
        access_token: '',
        refresh_token: '',
        is_editor: false,
        is_admin: false
      },
    players: [],
    competitions: [],
    seasons: [],
    opponents: []
  },
  getters: {
    activePlayers (state, getters) {
      return state.players.filter(player => player.active).sort(function (a, b) {
        if (a.name < b.name) {
          return -1
        }
        if (a.name > b.name) {
          return 1
        }
        return 0
      })
    },
    competitionsByDate (state, getters) {
      return state.competitions.sort(function (a, b) {
        if (a.start_date < b.start_date) {
          return 1
        }
        if (a.start_date > b.start_date) {
          return -1
        }
        return 0
      })
    },
    seasonsSorted (state, getters) {
      return state.seasons.sort(function (a, b) {
        if (a.name < b.name) {
          return -1
        }
        if (a.name > b.name) {
          return 1
        }
        return 0
      })
    },
    opponentsSorted (state, getters) {
      return state.opponents.sort(function (a, b) {
        if (a.name < b.name) {
          return -1
        }
        if (a.name > b.name) {
          return 1
        }
        return 0
      })
    }
  },
  mutations: {
    updateCurrentUser (state, user) {
      state.user = user
    },
    setPlayers (state, players) {
      state.players = players
    },
    setCompetitions (state, competitions) {
      state.competitions = competitions
    },
    setSeasons (state, seasons) {
      state.seasons = seasons
    },
    setOpponents (state, opponents) {
      state.opponents = opponents
    }
  },
  actions: {
    updateCurrentUser (context) {
      const user = JSON.parse(window.localStorage.getItem('user'))
      context.commit('updateCurrentUser', user)
      context.dispatch('init')
    },
    clearCurrentUser (context) {
      const user = {
        username: '',
        access_token: '',
        refresh_token: '',
        is_editor: false,
        is_admin: false
      }
      window.localStorage.setItem('user', JSON.stringify(user))
      context.commit('updateCurrentUser', user)
      context.commit('setPlayers', [])
      context.commit('setCompetitions', [])
      context.commit('setSeasons', [])
      context.commit('setOpponents', [])
    },
    init (context) {
      const user = JSON.parse(window.localStorage.getItem('user'))
      if (user === null || user === undefined) {
        router.push('/login')
      } else {
        context.dispatch('fetchPlayers')
        context.dispatch('fetchCompetitions')
        context.dispatch('fetchSeasons')
        context.dispatch('fetchOpponents')
        context.commit('updateCurrentUser', user)
      }
    },
    fetchPlayers ({ commit }) {
      API.getPlayers().then(players => {
        commit('setPlayers', players)
      })
    },
    fetchCompetitions ({ commit }) {
      API.getCompetitions().then(competitions => {
        commit('setCompetitions', competitions)
      })
    },
    fetchSeasons ({ commit }) {
      API.getSeasons().then(seasons => {
        commit('setSeasons', seasons)
      })
    },
    fetchOpponents ({ commit }) {
      API.getOpponents().then(opponents => {
        commit('setOpponents', opponents)
      })
    },
    createPlayer ({ commit, state, dispatch }, player) {
      // add team onto payload
      player.team = state.team
      API.createPlayer(player)
        .then(player => {
          router.push({
            name: 'Player',
            params: { id: player.id }
          })
          dispatch('fetchPlayers')
        })
    },
    createOpponent ({ commit, state, dispatch }, opponent) {
      // add team onto payload
      opponent.team = state.team

      API.createOpponent(opponent)
        .then(result => {
          router.push({
            name: 'Opponent',
            params: { id: result.id }
          })
          dispatch('fetchOpponents')
        })
    },
    createCompetition ({ commit, state, dispatch }, competition) {
      // add team onto payload
      competition.team = state.team

      API.createCompetition(competition)
        .then(result => {
          dispatch('fetchCompetitions')
          router.push({
            name: 'Competition',
            params: { id: result.id }
          })
        })
    },
    createSeason ({ commit, state, dispatch }, season) {
      // add team onto payload
      season.team = state.team

      API.createSeason(season)
        .then(result => {
          dispatch('fetchSeasons')
          router.push({
            name: 'Season',
            params: { id: result.id }
          })
        })
    },
    deleteCompetition ({ commit, state, dispatch }, id) {
      return new Promise((resolve, reject) => {
        API.deleteCompetition(id)
          .then((resp) => {
            dispatch('fetchCompetitions')
            router.push({
              name: 'Competitions'
            })
            resolve(resp)
          }, error => {
            reject(error)
          })
      })
    },
    deleteSeason ({ commit, state, dispatch }, id) {
      return new Promise((resolve, reject) => {
        API.deleteSeason(id)
          .then((resp) => {
            dispatch('fetchSeasons')
            router.push({
              name: 'Seasons'
            })
            resolve(resp)
          }, error => {
            reject(error)
          })
      })
    },
    deleteOpponent ({ commit, state, dispatch }, id) {
      return new Promise((resolve, reject) => {
        API.deleteOpponent(id)
          .then((resp) => {
            dispatch('fetchOpponents')
            router.push({
              name: 'Opponents'
            })
            resolve(resp)
          }, error => {
            reject(error)
          })
      })
    }
  }
})
