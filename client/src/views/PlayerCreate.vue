<template>
    <player-form :player="player"
                 :onSubmit="submit"

    ></player-form>
</template>

<script>
import PlayerForm from '@/components/forms/PlayerForm'

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
      this.$store.dispatch('createPlayer', this.player)
    }
  }
}
</script>
