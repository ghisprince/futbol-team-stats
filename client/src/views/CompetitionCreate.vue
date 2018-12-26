<template>
    <CompetitionForm :competition="competition"
                     :onSubmit="submit"

    ></CompetitionForm>
</template>

<script>
import CompetitionForm from '@/components/forms/CompetitionForm'

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
      this.$store.dispatch('createCompetition', this.competition)
    }
  }
}
</script>
