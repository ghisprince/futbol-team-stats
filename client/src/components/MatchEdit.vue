<template>
    <match-form :match="match"
                :onSubmit="submit"
                :onCancel="cancel"
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
      match: {}
    }
  },
  mounted () {
    const { id } = this.$route.params
    this.load(id)
  },
  methods: {
    submit () {
      API.updateMatch(this.match.id, this.match)
        .then(() => {
          this.$router.push({
            name: 'Match',
            params: { id: this.match.id }})
        })
    },
    cancel () {
      this.$router.push({
        name: 'Match',
        params: { id: this.match.id }})
    },
    load (id) {
      API.getMatch(id)
        .then((match) => {
          this.match = match
        })
    }
  }
}
</script>
