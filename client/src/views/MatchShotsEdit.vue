<template>
  <div>
    <shots-form
               :player_matches="player_matches"
               :onSubmit="submit"
               :onCancel="cancel">
    </shots-form>
  </div>
</template>

<script>
import ShotsForm from '@/components/forms/ShotsForm'
import API from '@/lib/API'

export default {
  components: {
    ShotsForm
  },
  data () {
    return {
      player_matches: {},
      shots: []
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
            params: { id: this.player_matches[0].match }
          })
        })
    },
    cancel () {
      this.$router.push({
        name: 'Match',
        params: { id: this.player_matches[0].id }
      })
    },
    load (id) {
      API.getPlayerMatchesByMatch(id)
        .then((player_matches) => {
          this.player_matches = player_matches
        })
      API.getShotsByMatch(id)
        .then((shots) => {
          this.shots = shots
        })
    }
  }
}
</script>
