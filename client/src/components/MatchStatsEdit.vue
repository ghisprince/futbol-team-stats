<template>
    <match-stats-form
               :match_stats="match_stats"
               :onSubmit="submit"
               :onCancel="cancel"
    ></match-stats-form>
</template>

<script>
import MatchStatsForm from '@/components/forms/MatchStatsForm'
import API from '@/lib/API'

export default {
  components: {
    MatchStatsForm
  },
  data () {
    return {
      match_stats: {}
    }
  },
  mounted () {
    // TODO: actually could do like PlayerMatchEdit where id is
    //  the match id and that's what we query
    const { id } = this.$route.params
    this.load(id)
  },
  methods: {
    submit () {
      API.updateMatchStats(this.match_stats.id, this.match_stats)
        .then(() => {
          this.$router.push({
            name: 'Match',
            params: { id: this.match_stats.match }})
        })
    },
    cancel () {
      this.$router.push({
        name: 'Match',
        params: { id: this.match_stats.id }})
    },
    load (id) {
      API.getMatchStats(id)
        .then((match_stats) => {
          this.match_stats = match_stats
        })
    }
  }
}
</script>
