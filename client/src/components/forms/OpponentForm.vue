<template>
<v-card>
  <v-container>
    <v-card>
      <v-form ref="form" v-model="valid" lazy-validation>

        <v-text-field
          v-model="opponent.name"
          :rules="nameRules"
          :counter="50"
          label="Name"
          required>
        </v-text-field>

        <v-textarea
          v-model="opponent.note"
          label="Note">
        </v-textarea>

        <v-text-field
          v-model="opponent.external_url"
          label="Opponent URL">
        </v-text-field>

        <v-btn :disabled="!valid" @click="submit">submit</v-btn>
        <v-btn @click="clear">clear</v-btn>
      </v-form>
    </v-card>
  </v-container>
</v-card>
</template>

<script>

export default {
  props: ['opponent', 'onSubmit'],
  data: () => ({
    valid: true,
    nameRules: [
      v => (v && v.trim().length !== 0) || 'Name is required yo',
      v => !!v || 'Name is required',
      v => (v && v.length <= 50) || 'Name must be less than 40 characters'
    ]
  }),
  methods: {
    submit () {
      if (this.valid) {
        this.onSubmit()
      }
    },
    clear () {
      this.$refs.form.reset()
    }
  }
}
</script>
