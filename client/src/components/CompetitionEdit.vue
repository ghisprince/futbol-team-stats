<template>
    <CompetitionForm :competition="competition"
                     :onSubmit="submit"
    ></CompetitionForm>
</template>

<script>
import CompetitionForm from '@/components/forms/CompetitionForm'
import API from '@/lib/API'

export default {
  components: {
    CompetitionForm
  },
  data () {
    return {
      competition: {}
    }
  },
  mounted () {
    const { id } = this.$route.params
    this.load(id)
  },
  methods: {
    submit () {
      API.updateCompetition(this.competition.id, this.competition)
        .then(() => {
          this.$router.push({
            name: 'Competition',
            params: { id: this.competition.id }})
        })
    },
    load (id) {
      API.getCompetition(id)
        .then((competition) => {
          this.competition = competition
        })
    }
  }
}
</script>
