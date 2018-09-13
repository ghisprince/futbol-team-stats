import axios from 'axios'

const competitionsURL = '/api/v1/competitions/'
const matchesURL = '/api/v1/matches/'
const opponentsURL = '/api/v1/opponents/'
const playerMatchesURL = '/api/v1/playermatches/'
const matchStatsURL = '/api/v1/matchstats/'
const playersURL = '/api/v1/players/'

export default {
  //  competitions
  getCompetitions () {
    return axios.get(competitionsURL)
      .then(response => response.data)
  },
  getCompetition (id) {
    return axios.get(`${competitionsURL}/${id}`)
      .then(response => response.data)
  },
  createCompetition (competition) {
    return axios.post(competitionsURL, competition)
      .then(response => response.data)
  },
  updateCompetition (id, competition) {
    return axios.patch(`${competitionsURL}/${id}`, competition)
      .then(response => response.data)
  },
  deleteCompetition (id) {
    return axios.delete(`${competitionsURL}/${id}`)
      .then(response => response.data)
  },
  //  matches
  getMatchesByCompetition (id) {
    return axios.get(`${matchesURL}/?competition_id=${id}`)
      .then(response => response.data)
  },
  getMatchesByOpponent (id) {
    return axios.get(`${matchesURL}/?opponent_id=${id}`)
      .then(response => response.data)
  },
  // Match
  getMatch (id) {
    return axios.get(`${matchesURL}/${id}`)
      .then(response => response.data)
  },
  createMatch (match) {
    return axios.post(matchesURL, match)
      .then(response => response.data)
  },
  updateMatch (id, match) {
    return axios.patch(`${matchesURL}/${id}`, match)
      .then(response => response.data)
  },
  deleteMatch (id) {
    return axios.delete(`${matchesURL}/${id}`)
      .then(response => response.data)
  },
  // MatchStats  ( no return, data is accessed on match? )
  getMatchStats (id) {
    return axios.get(`${matchStatsURL}/${id}`)
      .then(response => response.data)
  },
  createMatchStats (match_stats) {
    return axios.post(matchStatsURL, match_stats)
      .then(response => response.data)
  },
  updateMatchStats (id, match) {
    return axios.patch(`${matchStatsURL}/${id}`, match)
      .then(response => response.data)
  },
  // Opponents
  getOpponents () {
    return axios.get(opponentsURL)
      .then(response => response.data)
  },
  getOpponent (id) {
    return axios.get(`${opponentsURL}/${id}`)
      .then(response => response.data)
  },
  createOpponent (opponent) {
    return axios.post(opponentsURL, opponent)
      .then(response => response.data)
  },
  updateOpponent (id, opponent) {
    return axios.patch(`${opponentsURL}/${id}`, opponent)
      .then(response => response.data)
  },
  deleteOpponent (id) {
    return axios.delete(`${opponentsURL}/${id}`)
      .then(response => response.data)
  },
  // playerMatches
  createPlayerMatch (player_match) {
    return axios.post(playerMatchesURL, player_match)
      .then(response => response.data)
  },
  updatePlayerMatch (id, player_match) {
    return axios.patch(`${playerMatchesURL}/${id}`, player_match)
      .then(response => response.data)
  },
  deletePlayerMatch (id) {
    return axios.delete(`${playerMatchesURL}/${id}`)
      .then(response => response.data)
  },
  getPlayerMatchesByMatch (id) {
    return axios.get(`${playerMatchesURL}/?match_id=${id}`)
      .then(response => response.data)
  },
  getPlayerMatchesByCompetition (id) {
    return axios.get(`${playerMatchesURL}/?competition_id=${id}`)
      .then(response => response.data)
  },
  getPlayerMatchesByOpponent (id) {
    return axios.get(`${playerMatchesURL}/?opponent_id=${id}`)
      .then(response => response.data)
  },
  getPlayerMatchesByPlayer (id) {
    return axios.get(`${playerMatchesURL}/?player_id=${id}`)
      .then(response => response.data)
  },
  getPlayerMatchesByPlayerEx (id) {
    return axios.get(`${playerMatchesURL}/?player_id=${id}&expand=true`)
      .then(response => response.data)
  },
 
  // players
  getPlayers () {
    return axios.get(playersURL)
      .then(response => response.data)
  },
  getPlayer (id) {
    return axios.get(`${playersURL}/${id}`)
      .then(response => response.data)
  },
  createPlayer (player) {
    return axios.post(playersURL, player)
      .then(response => response.data)
  },
  updatePlayer (id, player) {
    return axios.patch(`${playersURL}/${id}`, player)
      .then(response => response.data)
  },
  deletePlayer (id) {
    return axios.delete(`${playersURL}/${id}`)
      .then(response => response.data)
  }
}
