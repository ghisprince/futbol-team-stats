<template>
    <SeasonForm :season="season"
                :onSubmit="submit">
    </SeasonForm>
</template>

<script>
import SeasonForm from '@/components/forms/SeasonForm'
import API from '@/lib/API'

export default {
  components: {
    SeasonForm
  },
  data () {
    return {
      season: {}
    }
  },
  mounted () {
    const { id } = this.$route.params
    this.load(id)
  },
  methods: {
    submit () {
      API.updateSeason(this.season.id, this.season)
        .then(() => {
          this.$router.push({
            name: 'Season',
            params: { id: this.season.id }
          })
        })
        .then(
          this.$store.dispatch('fetchSeasons')
        )
    },
    load (id) {
      API.getSeason(id)
        .then((season) => {
          this.season = season
        })
    }
  }
}
</script>
