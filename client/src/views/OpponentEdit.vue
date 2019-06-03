<template>
    <OpponentForm :opponent="opponent"
                  :onSubmit="submit"
    ></OpponentForm>
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
      opponent: {}
    }
  },
  mounted () {
    const { id } = this.$route.params
    this.load(id)
  },
  methods: {
    submit () {
      API.updateOpponent(this.opponent.id, this.opponent)
        .then(() => {
          this.$router.push({
            name: 'Opponent',
            params: { id: this.opponent.id }
          })
        })
        .then(
          this.$store.dispatch('fetchOpponents')
        )
    },
    load (id) {
      API.getOpponent(id)
        .then((opponent) => {
          this.opponent = opponent
        })
    }
  }
}
</script>
