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
      competition: {
        name: '',
        result: '',
        note: '',
        external_url: ''
      }

    }
  },
  methods: {
    submit () {
      this.competition.team = this.$store.state.team
      API.createCompetition(this.competition)
        .then(result => {
          this.$router.push({
            name: 'Competition',
            params: { id: result.id }})
        })
    }
  }
}
</script>
