<template>
    <match-form :match="match"
                :onSubmit="submit"
    ></match-form>
</template>

<script>
import MatchForm from '@/components/forms/MatchForm'
import API from '@/lib/API'

function today() {
    var d = new Date(Date.now()),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2) month = '0' + month;
    if (day.length < 2) day = '0' + day;

    return [year, month, day].join('-') + "T10:00:00";
}

export default {
  components: {
    MatchForm
  },
  data () {
    return {
      match: {
        date_time: today(),
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
