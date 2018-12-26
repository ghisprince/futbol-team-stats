<template>
    <player-form :player="player"
                 :onSubmit="submit"
    ></player-form>
</template>

<script>
import PlayerForm from '@/components/forms/PlayerForm'
import API from '@/lib/API'

export default {
  components: {
    PlayerForm
  },
  data () {
    return {
      player: {}
    }
  },
  mounted () {
    const { id } = this.$route.params
    this.load(id)
  },
  methods: {
    submit () {
      API.updatePlayer(this.player.id, this.player)
        .then(() => {
          this.$router.push({
            name: 'Player',
            params: { id: this.player.id }})
        })
        .then(
          this.$store.dispatch('fetchPlayers')
        )
    },
    load (id) {
      API.getPlayer(id)
        .then((player) => {
          this.player = player
        })
    }
  }
}
</script>
