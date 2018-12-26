<template>
  <div>
    <v-toolbar>
      <h2>Shots</h2>
      <v-divider class="mx-2" inset vertical></v-divider>
      <v-spacer></v-spacer>

      <!-- THIS IS POPUP DIALOG -->
      <v-dialog v-model="dialog" max-width="600px">
        <v-btn slot="activator" color="primary" @click="newItem" dark class="mb-2">New Shot</v-btn>
        <v-card>
          <v-card-title>
            <span class="headline">{{ formTitle }}</span>
          </v-card-title>

          <v-card-text v-if="Array.isArray(this.player_matches)">
            <v-container grid-list-md>
              <v-layout wrap>
                <v-flex>
                  <v-select
                    v-model="editedItem.player_match"
                    :items="player_matches_sorted"
                    item-text="player_label"
                    item-value="id"
                    :rules="[v => !!v || 'Player is required']"
                    label="Player"
                    required
                  >
                  </v-select>
                </v-flex>
              </v-layout>
              <v-layout wrap>
                <v-flex>
                  <v-checkbox v-model="editedItem.by_opponent"
                              label="By Opponent">
                  </v-checkbox>
                </v-flex>

                <v-flex>
                  <v-checkbox v-model="editedItem.on_target"
                              label="On Target">
                  </v-checkbox>
                </v-flex>

                <v-flex>
                  <v-checkbox v-model="editedItem.pk"
                              label="Penalty Kick">
                  </v-checkbox>
                </v-flex>

              </v-layout>
              <v-layout wrap>

                <v-flex>
                  <v-checkbox v-model="editedItem.scored"
                              label="Scored"></v-checkbox>
                </v-flex>

                <v-flex v-if="editedItem.scored">
                  <v-text-field
                    v-model="editedGoal.time"
                    label="Goal Time"
                    mask="##">
                  </v-text-field>
                </v-flex>
              </v-layout>

              <v-layout wrap v-if="editedItem.scored && !editedItem.by_opponent">
                <v-flex>
                  <v-checkbox v-model="editedGoal.assisted"
                              label="Assisted"></v-checkbox>
                </v-flex>

                <v-flex v-if="editedGoal.assisted">
                  <v-select
                    v-model="editedAssist.player_match"
                    :items="player_matches"
                    item-text="player_label"
                    item-value="id"
                    label="Assist Player"
                    required
                  >
                  </v-select>
                </v-flex>

              </v-layout>
              <v-layout wrap>
                <h1>Shot location</h1>
                <br/>
                <p>Click to move active (Yellow) shot</p>
                <br/>
                <shots-graph :shots="shots"
                             :activeShotId="editedItem.id"
                             :onClickShot=onClickShot
                             :onClickCanvas=onClickCanvas
                             :showHiddenArea="true"
                >
                </shots-graph>
              </v-layout>

            </v-container>
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" flat @click.native="close">Cancel</v-btn>
            <v-btn color="blue darken-1" flat @click.native="save">Save</v-btn>
          </v-card-actions>

        </v-card>
      </v-dialog>
    </v-toolbar>

    <!-- THIS IS THE TABLE -->
    <v-data-table v-if="Array.isArray(this.shots)"
      :headers="headers"
      :items="shots"
      hide-actions
    >
      <template slot="items" slot-scope="props">
        <td>{{ props.item.player_label }}</td>
        <td><v-icon v-show="props.item.by_opponent">done</v-icon></td>
        <td><v-icon v-show="props.item.on_target">done</v-icon></td>
        <td><v-icon v-show="props.item.pk">done</v-icon></td>
        <td><v-icon v-show="props.item.scored">done</v-icon></td>

        <td>
          <v-icon
            small
            class="mr-2"
            @click="editItem(props.item)"
          >
            edit
          </v-icon>
          <v-icon
            small
            @click="deleteItem(props.item)"
          >
            delete
          </v-icon>
        </td>

      </template>
      <template slot="no-data">
        <v-btn color="primary" @click="initialize">Reset</v-btn>
      </template>
    </v-data-table>
    <shots-graph :shots="shots"
      :onClickShot=onClickShot
      :showHiddenArea="true"
    ></shots-graph>
    <v-btn @click="backToMatch()" color="error">Back To Match</v-btn>
  </div>
</template>

<script>
import API from '@/lib/API'
import ShotsGraph from '@/components/ShotsGraph'

export default {
  props: ['match_id', 'player_matches', 'onSubmit', 'onCancel'],
  components: {
    ShotsGraph
  },
  data: () => ({
    dialog: false,
    shots: [],
    headers: [
      {
        text: 'Player',
        value: 'player_label'
      },
      {
        text: 'By Opponent',
        value: 'by_opponent'
      },
      {
        text: 'On Target',
        value: 'on_target'
      },
      {
        text: 'Penalty Kick',
        value: 'pk'
      },
      {
        text: 'Scored',
        value: 'scored'
      },
      {
        text: 'Actions',
        value: 'actions'
      }

    ],
    editedIndex: -1,
    editedItem: {
      id: -1,
      player_match: '',
      player_label: '',
      by_opponent: false,
      on_target: false,
      pk: false,
      scored: false
    },
    defaultItem: {
      player_match: '',
      player_label: '',
      by_opponent: false,
      on_target: false,
      pk: false,
      scored: false
    },
    editedGoal: {
      time: 0,
      assisted: false
    },
    defaultGoal: {
      time: 0,
      assisted: false
    },
    editedAssist: {
      id: '',
      player_match: '',
      player_label: ''
    },
    defaultAssist: {
      id: '',
      player_match: '',
      player_label: ''
    },
    valid: true
  }),
  computed: {
    formTitle () {
      return this.editedIndex === -1 ? 'New Player Shot' : 'Edit Player Shot'
    },
    player_matches_sorted () {
      let pms = this.player_matches.slice()
      return pms.sort(function (a, b) {
        if (a.player_label < b.player_label) {
          return -1
        }
        if (a.player_label > b.player_label) {
          return 1
        }
        return 0
      })
    }
  },
  watch: {
    dialog (val) {
      val || this.close()
    }
  },
  mounted () {
    const { id } = this.$route.params
    this.load(id)
  },
  methods: {
    onClickShot (shot) {
      this.editItem(shot)
    },
    onClickCanvas (x, y) {
      this.editedItem.x = x
      this.editedItem.y = y
    },
    load (id) {
      API.getShotsByMatch(id)
        .then((shots) => {
          this.shots = shots
        })
    },
    submit () {
      if (this.valid) {
        this.onSubmit()
      }
    },
    cancel () {
      this.onCancel()
    },
    newItem () {
      this.editedItem = Object.assign({}, this.defaultItem)
    },
    editItem (item) {
      this.editedIndex = this.shots.indexOf(item)
      this.editedGoal = Object.assign({}, this.defaultGoal)
      this.editedAssist = Object.assign({}, this.defaultAssist)
      Object.assign(this.editedItem, item)
      Object.assign(this.editedGoal, item.goal)
      if (item.goal && item.goal.assist) {
        Object.assign(this.editedAssist, item.goal.assist)
      }
      this.dialog = true
    },
    deleteItem (item) {
      // TODO: actually remove the shot ??
      const id = item.id
      const index = this.shots.indexOf(item)

      if (index > -1) {
        this.shots.splice(index, 1)
      } 
      API.deleteShot(id)
    },
    close () {
      this.dialog = false
      setTimeout(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      }, 300)
    },
    initialize () {},
    save () {
      if (this.editedItem.scored) {
        this.editedItem.goal = this.editedGoal
      }
      if (this.editedItem.scored && this.editedGoal.assisted) {
        this.editedItem.goal.assist = this.editedAssist
      }

      if (this.editedIndex > -1) {
        let editedIndex = this.editedIndex

        // updated existing Shot
        API.updateShot(this.editedItem.id, this.editedItem)
          .then((shot) => {
            Object.assign(this.shots[editedIndex], shot)
          })
      } else {
        // create new Shot
        const match_id = this.$route.params.id
        this.editedItem.match = match_id
        API.createShot(this.editedItem)
          .then((shot) => {
            this.shots.push(shot)
          })
      }
      this.close()
    },
    backToMatch () {
      // TODO: put this into a prop
      const match_id = this.$route.params.id

      this.$router.push({
        name: 'Match',
        params: { id: match_id }
      })
    }
  }
}

</script>
