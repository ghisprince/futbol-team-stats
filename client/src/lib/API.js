import axios from 'axios'
import router from '@/router'

const loginURL = 'login'
const competitionsURL = 'competitions'
const matchesURL = 'matches'
const opponentsURL = 'opponents'
const seasonsURL = 'seasons'
const playerMatchesURL = 'playermatches'
const matchStatsURL = 'matchstats'
const playersURL = 'players'
const shotsURL = 'shots'
const playerseasondataURL = 'playerseasondata'
const teamseasondataURL = 'teamseasondata'

const getHeader = function () {
  const user = JSON.parse(window.localStorage.getItem('user'))

  try {
    if (user.refresh_token) {
      return 'Bearer ' + user.refresh_token
    }
    throw new Error('error')
  } catch (err) {
    return ''
  }
}

const HTTP = axios.create({
  baseURL: 'api/',
  headers: { 'Authorization': getHeader() }
})

HTTP.interceptors.response.use(
  function (response) { return response },
  function (error) {
    if (error.response) {
      if (error.response.status === 401) {
        router.push({ name: 'login' })
      }
      return Promise.reject(error)
    }
  }
)

export default {
  HTTP,
  logIn (username, password) {
    return HTTP.post(loginURL, { username: username, password: password })
      .then(function (response) {
        const user = {}
        user.username = response.data.username
        user.access_token = response.data.access_token
        user.refresh_token = response.data.refresh_token
        user.is_editor = response.data.is_editor
        user.is_admin = response.data.is_admin
        window.localStorage.setItem('user', JSON.stringify(user))
        HTTP.defaults.headers['Authorization'] = getHeader()
        return response.data
      })
  },
  logout () {
    HTTP.defaults.headers['Authorization'] = ''
  },
  //  competitions
  getCompetitions () {
    return HTTP.get(competitionsURL)
      .then(response => response.data)
  },
  getCompetition (id) {
    return HTTP.get(`${competitionsURL}/${id}`)
      .then(response => response.data)
  },
  createCompetition (competition) {
    return HTTP.post(competitionsURL, competition)
      .then(response => response.data)
  },
  updateCompetition (id, competition) {
    return HTTP.patch(`${competitionsURL}/${id}`, competition)
      .then(response => response.data)
  },
  deleteCompetition (id) {
    return HTTP.delete(`${competitionsURL}/${id}`)
      .then(response => response.data)
  },
  //  matches
  getMatchesByCompetition (id) {
    return HTTP.get(`${matchesURL}?competition_id=${id}`)
      .then(response => response.data)
  },
  getMatchesByOpponent (id) {
    return HTTP.get(`${matchesURL}?opponent_id=${id}`)
      .then(response => response.data)
  },
  // Match
  getMatch (id) {
    return HTTP.get(`${matchesURL}/${id}`)
      .then(response => response.data)
  },
  createMatch (match) {
    return HTTP.post(matchesURL, match)
      .then(response => response.data)
  },
  updateMatch (id, match) {
    return HTTP.patch(`${matchesURL}/${id}`, match)
      .then(response => response.data)
  },
  deleteMatch (id) {
    return HTTP.delete(`${matchesURL}/${id}`)
      .then(response => response.data)
  },
  // MatchStats  ( no return, data is accessed on match? )
  getMatchStats (id) {
    return HTTP.get(`${matchStatsURL}/${id}`)
      .then(response => response.data)
  },
  createMatchStats (match_stats) {
    return HTTP.post(matchStatsURL, match_stats)
      .then(response => response.data)
  },
  updateMatchStats (id, match) {
    return HTTP.patch(`${matchStatsURL}/${id}`, match)
      .then(response => response.data)
  },
  // Opponents
  getOpponents () {
    return HTTP.get(opponentsURL)
      .then(response => response.data)
  },
  getOpponent (id) {
    return HTTP.get(`${opponentsURL}/${id}`)
      .then(response => response.data)
  },
  createOpponent (opponent) {
    return HTTP.post(opponentsURL, opponent)
      .then(response => response.data)
  },
  updateOpponent (id, opponent) {
    return HTTP.patch(`${opponentsURL}/${id}`, opponent)
      .then(response => response.data)
  },
  deleteOpponent (id) {
    return HTTP.delete(`${opponentsURL}/${id}`)
      .then(response => response.data)
  },
  // Seasons
  getSeasons () {
    return HTTP.get(seasonsURL)
      .then(response => response.data)
  },
  getSeason (id) {
    return HTTP.get(`${seasonsURL}/${id}`)
      .then(response => response.data)
  },
  createSeason (season) {
    return HTTP.post(seasonsURL, season)
      .then(response => response.data)
  },
  updateSeason (id, season) {
    return HTTP.patch(`${seasonsURL}/${id}`, season)
      .then(response => response.data)
  },
  deleteSeason (id) {
    return HTTP.delete(`${seasonsURL}/${id}`)
      .then(response => response.data)
  },
  getPlayerSeasonData (id) {
    return HTTP.get(`${playerseasondataURL}/${id}`)
      .then(response => response.data)
  },
  getTeamSeasonData (id) {
    return HTTP.get(`${teamseasondataURL}/${id}`)
      .then(response => response.data)
  },

  // playerMatches
  createPlayerMatch (player_match) {
    return HTTP.post(playerMatchesURL, player_match)
      .then(response => response.data)
  },
  updatePlayerMatch (id, player_match) {
    return HTTP.patch(`${playerMatchesURL}/${id}`, player_match)
      .then(response => response.data)
  },
  deletePlayerMatch (id) {
    return HTTP.delete(`${playerMatchesURL}/${id}`)
      .then(response => response.data)
  },
  getPlayerMatchesByMatch (id) {
    return HTTP.get(`${playerMatchesURL}?match_id=${id}`)
      .then(response => response.data)
  },
  getPlayerMatchesByCompetition (id) {
    return HTTP.get(`${playerMatchesURL}?competition_id=${id}`)
      .then(response => response.data)
  },
  getPlayerMatchesByOpponent (id) {
    return HTTP.get(`${playerMatchesURL}?opponent_id=${id}`)
      .then(response => response.data)
  },
  getPlayerMatchesByPlayer (id) {
    return HTTP.get(`${playerMatchesURL}?player_id=${id}`)
      .then(response => response.data)
  },
  getPlayerMatchesByPlayerEx (id) {
    return HTTP.get(`${playerMatchesURL}?player_id=${id}&expand=true`)
      .then(response => response.data)
  },

  // players
  getPlayers () {
    return HTTP.get(playersURL)
      .then(response => response.data)
  },
  getPlayer (id) {
    return HTTP.get(`${playersURL}/${id}`)
      .then(response => response.data)
  },
  createPlayer (player) {
    return HTTP.post(playersURL, player)
      .then(response => response.data)
  },
  updatePlayer (id, player) {
    return HTTP.patch(`${playersURL}/${id}`, player)
      .then(response => response.data)
  },
  deletePlayer (id) {
    return HTTP.delete(`${playersURL}/${id}`)
      .then(response => response.data)
  },
  // shots
  getShotsByMatch (id) {
    return HTTP.get(`${shotsURL}?match_id=${id}`)
      .then(response => response.data)
  },
  getShotsByCompetition (id) {
    return HTTP.get(`${shotsURL}?competition_id=${id}`)
      .then(response => response.data)
  },
  getShotsByPlayer (id) {
    return HTTP.get(`${shotsURL}?player_id=${id}`)
      .then(response => response.data)
  },
  // todo: is this even used?
  getShotsByMatchEx (id) {
    return HTTP.get(`${shotsURL}?match_id=${id}&expand=true`)
      .then(response => response.data)
  },
  createShot (shot) {
    if (shot.id === -1) { delete shot.id }

    return HTTP.post(shotsURL, shot)
      .then(response => response.data)
  },
  updateShot (id, shot) {
    return HTTP.patch(`${shotsURL}/${id}`, shot)
      .then(response => response.data)
  },
  deleteShot (id) {
    return HTTP.delete(`${shotsURL}/${id}`)
      .then(response => response.data)
  }

}
