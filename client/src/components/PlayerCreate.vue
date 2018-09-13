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
      player: {
        name: '',
        number: '',
        active: true
      }

    }
  },
  methods: {
    submit () {
      this.player.team = this.$store.state.team
      API.createPlayer(this.player)
        .then(player => {
          this.$router.push({
            name: 'Player',
            params: { id: player.id }})
        })
    }
  }
}
</script>
