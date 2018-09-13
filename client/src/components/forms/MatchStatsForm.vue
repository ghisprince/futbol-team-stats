<template>
  <v-layout>
    <v-flex xs12>

      <v-form ref="form" v-model="valid" lazy-validation>
        <h2>Opponent stats</h2>
        <v-text-field
        v-model="match_stats.opponent_corners"
        label="Opponent corners"
        type="number"
        ></v-text-field>

        <v-text-field
        v-model="match_stats.opponent_yellow_cards"
        label="Opponent yellow cards"
        type="number"
        ></v-text-field>

        <v-text-field
        v-model="match_stats.opponent_red_cards"
        label="Opponent red cards"
        type="number"
        default=0
        ></v-text-field>

        <v-btn :disabled="!valid" @click="submit">submit</v-btn>
        <v-btn @click="cancel">cancel</v-btn>
      </v-form>
    </v-flex>
  </v-layout>

</template>

<script>

export default {
  props: ['match_stats', 'onSubmit', 'onCancel'],
  data: () => ({
    valid: true
  }),
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
