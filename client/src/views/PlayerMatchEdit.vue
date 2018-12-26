<template>
    <player-matches-form
               :player_matches="player_matches"
               :onSubmit="submit"
               :onCancel="cancel"
    ></player-matches-form>
</template>

<script>
import PlayerMatchesForm from '@/components/forms/PlayerMatchesForm'
import API from '@/lib/API'

export default {
  components: {
    PlayerMatchesForm
  },
  data () {
    return {
      player_matches: {}
    }
  },
  mounted () {
    const { id } = this.$route.params
    this.load(id)
  },
  methods: {
    submit () {
      API.updatePlayerMatches(this.player_matches.id, this.player_matches)
        .then(() => {
          this.$router.push({
            name: 'Match',
            params: { id: this.player_matches[0].match }})
        })
    },
    cancel () {
      this.$router.push({
        name: 'Match',
        params: { id: this.player_matches[0].id }})
    },
    load (id) {
      API.getPlayerMatchesByMatch(id)
        .then((player_matches) => {
          this.player_matches = player_matches
        })
    }
  }
}
</script>
