import Vue from 'vue'
import Vuex from 'vuex'
import API from '@/lib/API'
import router from '@/router'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    team: {id: 1},
    authUser:
      { username: '',
        token: '',
        canEdit: false
      },
    players: [],
    competitions: [],
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
      state.authUser = user
    },
    setPlayers (state, players) {
      state.players = players
    },
    setCompetitions (state, competitions) {
      state.competitions = competitions
    },
    setOpponents (state, opponents) {
      state.opponents = opponents
    }
  },
  actions: {
    updateCurrentUser (context) {
      const user = JSON.parse(window.localStorage.getItem('futUser'))
      context.commit('updateCurrentUser', user)
      context.dispatch('init')
    },
    init (context) {
      const authUser = JSON.parse(window.localStorage.getItem('futUser'))
      if (authUser === null || authUser === undefined) {
        router.push('/login')
      } else {
        context.dispatch('fetchPlayers')
        context.dispatch('fetchCompetitions')
        context.dispatch('fetchOpponents')
        context.commit('updateCurrentUser', authUser)
      }
    },
    fetchPlayers ({commit}) {
      API.getPlayers().then(players => {
        commit('setPlayers', players)
      })
        .catch((err) => {
          if (err.response.status === 401) {
            router.push({name: 'login'})
          }
        })
    },
    fetchCompetitions ({commit}) {
      API.getCompetitions().then(competitions => {
        commit('setCompetitions', competitions)
      })
    },
    fetchOpponents ({commit}) {
      API.getOpponents().then(opponents => {
        commit('setOpponents', opponents)
      })
    },
    createPlayer ({commit, state, dispatch}, player) {
      // add team onto payload
      player.team = state.team
      API.createPlayer(player)
        .then(player => {
          router.push({
            name: 'Player',
            params: { id: player.id }})
          dispatch('fetchPlayers')
        })
    },
    createOpponent ({commit, state, dispatch}, opponent) {
      // add team onto payload
      opponent.team = state.team

      API.createOpponent(opponent)
        .then(result => {
          router.push({
            name: 'Opponent',
            params: { id: result.id }})
          dispatch('fetchOpponents')
        })
    },
    createCompetition ({commit, state, dispatch}, competition) {
      // add team onto payload
      competition.team = state.team

      API.createCompetition(competition)
        .then(result => {
          dispatch('fetchCompetitions')
          router.push({
            name: 'Competition',
            params: { id: result.id }})
        })
    },
    deleteCompetition ({commit, state, dispatch}, id) {
      return new Promise((resolve, reject) => {
        console.log(id)
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
    deleteOpponent ({commit, state, dispatch}, id) {
      return new Promise((resolve, reject) => {
        console.log(id)
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
