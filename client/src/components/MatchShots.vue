<template>
  <div>
    <v-card>
      <v-card-title>
        Shots yo!

      <v-spacer></v-spacer>
      <v-btn 
        :to="{
          name: 'MatchShotsEdit',
          params: {
              id: match_id
          }
        }"
        color="primary">Edit Shots</v-btn>
      </v-card-title>

      <v-flex>
        <shots-graph v-if="shots"
          :shots="shots"
          :text="text">
        </shots-graph>
      </v-flex>
      
    </v-card>
  </div>  
</template>

<script>
import API from '@/lib/API'
import ShotsGraph from '@/components/ShotsGraph'

export default {
  props: [ 'shots', 'match_id' ],
  data () {
    return {
      text: false
    }
  },
  methods: {
    editMatchShots () {
      alert("needs implementation!")
    }
  },
  components: {
    ShotsGraph
  },
  mounted () {
    this.load()
  },
  methods: {
    load () {
    }
  }
}
</script>

