<template>
  <div>
    <v-flex>
      <shots-graph v-if="shots"
        :shots="shots"
        :text="text"
        :selectedShotId="selectedShotId">
      </shots-graph>
    </v-flex>
      
  </div>  
</template>

<script>
import API from '@/lib/API'
import ShotsGraph from '@/components/ShotsGraph'

// TODO: drop this component? 
// it  does nothing. Just passes everything to ShotsGraph!

export default {
  props: [ 'shots', 'selectedShotId'],
  data () {
    return {
      text: false
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

