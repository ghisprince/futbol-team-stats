<template>
    <match-form :match="match"
                :onSubmit="submit"
    ></match-form>
</template>

<script>
import MatchForm from '@/components/forms/MatchForm'
import API from '@/lib/API'

export default {
  components: {
    MatchForm
  },
  data () {
    return {
      match: {
        date_time: '2018-10-20T12:20:00', // TODO today
        at_home: null,
        duration: 80,
        note: null
      }
    }
  },
  methods: {
    submit () {
      // add team onto payload
      this.match.team = this.$store.state.team
      API.createMatch(this.match)
        .then(result => {
          this.$router.push({
            name: 'Match',
            params: { id: result.id }})
        })
    }
  }
}
</script>
