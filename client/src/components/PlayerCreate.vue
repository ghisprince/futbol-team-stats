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
      this.$store.dispatch('createPlayer', this.player)
    }
  }
}
</script>
