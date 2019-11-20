<template>
    <SeasonForm :season="season"
                :onSubmit="submit">
    </SeasonForm>
</template>

<script>
import SeasonForm from '@/components/forms/SeasonForm'

export default {
  components: {
    SeasonForm
  },
  data () {
    return {
      season: {
        name: '',
        note: ''
      }

    }
  },
  methods: {
    submit () {
      this.$store.dispatch('createSeason', this.season)
    }
  }
}
</script>
