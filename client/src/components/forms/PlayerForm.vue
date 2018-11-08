<template>
  <v-card>
    <v-container>
      <v-card>

        <v-form ref="form" v-model="valid" lazy-validation>

          <v-text-field
            v-model="player.name"
            :rules="nameRules"
            :counter="30"
            label="Name"
            required>
          </v-text-field>

          <v-text-field
            v-model="player.number"
            label="Jersey Number"
            mask="###">
          </v-text-field>

          <v-checkbox
            v-model="player.active"
            label="Active">
          </v-checkbox>

          <v-btn :disabled="!valid" @click="submit">submit</v-btn>
          <v-btn @click="clear">clear</v-btn>
        </v-form>
      </v-card>
    </v-container>
  </v-card>  
</template>

<script>

export default {
  props: ['player', 'onSubmit'],
  data: () => ({
    valid: true,
    nameRules: [
      v => (v && v.trim().length !== 0) || 'Name is required yo',
      v => !!v || 'Name is required',
      v => (v && v.length <= 30) || 'Name must be less than 40 characters'
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
