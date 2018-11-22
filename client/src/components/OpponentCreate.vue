<template>
    <opponent-form :opponent="opponent"
                   :onSubmit="submit"

    ></opponent-form>
</template>

<script>
import OpponentForm from '@/components/forms/OpponentForm'

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
      this.$store.dispatch('createOpponent', this.opponent)
    }
  }
}
</script>
