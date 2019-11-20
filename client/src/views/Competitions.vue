<template id="competition-list">
  <v-card>
    <v-container>
      <v-card>
        <v-layout align-start justify-end fill-height>
          <v-btn v-if="is_editor"
                 color="success"
                 :to="{name: 'CompetitionCreate'}">
            NEW COMPETITION
          </v-btn>
        </v-layout>

        <v-card-title>
          <h2>Competitions</h2>
          <v-spacer></v-spacer>
          <v-text-field
            v-model="search"
            append-icon="search"
            label="Search"
            single-line>
          </v-text-field>
        </v-card-title>

      <!-- competition-table here -->
      <competitions-table :competitions="competitions"
                          :search="search"
                          :showProgress="showProgress"
      ></competitions-table>
      </v-card>
    </v-container>
  </v-card>
</template>

<script>
import CompetitionsTable from '@/components/CompetitionsTable'

export default {
  components: {
    CompetitionsTable
  },
  data () {
    return {
      showProgress: false,
      search: ''
      }
    }
  ,
  computed: {
    is_editor () {
      return this.$store.state.user.is_editor
    },
    competitions () {
      return this.$store.state.competitions
    }
  }
}
</script>
