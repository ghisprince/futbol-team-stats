<template>
  <v-container>
    <v-flex offset-xs1>
      <v-card v-on:keyup.enter="submit"
      >
        <v-alert type="error" :value="showError">
          Login failed
        </v-alert>
        <v-card-title primary-title>
          <h1>Login</h1>
          <v-spacer></v-spacer>
          <v-avatar size=80><img src="@/assets/crest.png"></v-avatar>
        </v-card-title>
        <v-form v-model="valid" lazy-validation>
          <v-text-field v-model="username"
                        name="Username"
                        label="Username"
                        :rules="[v => !!v || 'Username is required']"
                        required
                        prepend-icon="person" >
          </v-text-field>

          <v-text-field v-model="password"
                        name="Password"
                        label="Password"
                        type="password"
                        :rules="[v => !!v || 'Password is required']"
                        required
                        prepend-icon="lock">
          </v-text-field>

          <v-card-actions>
            <v-btn primary large block @click="submit">Login</v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
    </v-flex>
  </v-container>
</template>

<script>
import API from '@/lib/API'

export default {
  data: () => ({
    username: '',
    password: '',
    valid: true,
    showError: false
  }),

  methods: {
    submit () {
      var app = this
      const { username, password } = this
      API.logIn(username, password)
        .then(function (res) {
          app.$store.dispatch('init')
          app.$router.push({ name: 'Home' })
        })
        .catch((err) => {
          app.showError = true
        })
    }
  }
}
</script>
