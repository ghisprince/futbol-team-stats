<template>
  <v-card >
    <v-container>
      <v-card>
        <v-card-text>
          <v-form ref="form" v-model="valid" lazy-validation>
            <v-text-field
              v-model="match.date_time"
              label="Date"
              hint="2018-12-15T16:59:00"
              required
            ></v-text-field>

            <v-checkbox
              v-model="match.at_home"
              label="Home Game"
            ></v-checkbox>

            <v-text-field
              v-model="match.duration"
              label="Match duration"
              mask="##"
            ></v-text-field>

            <v-text-field
              v-model="match.external_url"
              label="Match URL">
            </v-text-field>

            <v-textarea
              v-model="match.note"
              label="Note"
            ></v-textarea>

            <v-select
              v-model="match.opponent"
              :items="opponents"
              item-text="name"
              item-value="id"
              :rules="[v => !!v || 'Opponent is required']"
              label="Opponent"
              required>
            </v-select>

            <v-select
              v-model="match.competition"
              :items="competitions"
              item-text="name"
              item-value="id"
              :rules="[v => !!v || 'Competition is required']"
              label="Competition"
              required
            >
            </v-select>

            <v-btn :disabled="!valid" @click="submit">submit</v-btn>
            <v-btn @click="cancel">cancel</v-btn>
          </v-form>
        </v-card-text>
      </v-card>
  </v-container>
</v-card>
</template>

<script>
export default {
  props: ['match', 'match_stats', 'onSubmit', 'onCancel'],
  data: () => ({
    valid: true
  }),
  computed: {
    competitions () {
      return this.$store.getters.competitionsByDate
    },
    opponents () {
      return this.$store.getters.opponentsSorted
    }
  },
  methods: {
    submit () {
      if (this.valid) {
        this.onSubmit()
      }
    },
    cancel () {
      this.onCancel()
    }
  }
}
</script>
