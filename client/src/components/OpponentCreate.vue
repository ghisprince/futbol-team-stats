<template>
    <opponent-form :opponent="opponent"
                   :onSubmit="submit"

    ></opponent-form>
</template>

<script>
import OpponentForm from '@/components/forms/OpponentForm'
import API from '@/lib/API'

export default {
  components: {
    OpponentForm
  },
  data () {
    return {
      opponent: {
        name: '',
        note: '',
        external_url: ''
      }

    }
  },
  methods: {
    submit () {
      // add team onto payload
      this.opponent.team = this.$store.state.team

      API.createOpponent(this.opponent)
        .then(result => {
          this.$router.push({
            name: 'Opponent',
            params: { id: result.id }})
        })
    }
  }
}
</script>
