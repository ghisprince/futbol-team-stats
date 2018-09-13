<template>
  <div>
    <v-toolbar>
      <h2>Player Match Stats</h2>
      <v-divider
        class="mx-2"
        inset
        vertical
      ></v-divider>
      <v-spacer></v-spacer>

      <!-- THIS IS POPUP DIALOG -->
      <v-dialog v-model="dialog" max-width="500px">
        <v-btn slot="activator" color="primary" dark class="mb-2">New Player Match</v-btn>
        <v-card>
          <v-card-title>
            <span class="headline">{{ formTitle }}</span>
          </v-card-title>

          <v-card-text>
            <v-container grid-list-md>
              <v-layout wrap>
                <v-flex>
                  <v-select
                    v-model="editedItem.player"
                    :items="players"
                    item-text="name"
                    item-value="id"
                    :rules="[v => !!v || 'Player is required']"
                    label="Player"
                    required
                  >
                  </v-select>
                </v-flex>

                <v-flex>
                  <v-checkbox v-model="editedItem.starter" label="Starter"></v-checkbox>
                </v-flex>

                <v-flex>
                  <v-text-field 
                    v-model="editedItem.minutes" 
                    label="Minutes Played"
                    mask="##">
                  </v-text-field>
                </v-flex>

                <v-flex>
                  <v-text-field 
                    v-model="editedItem.corners" 
                    label="Corners"
                    mask="##">
                </v-text-field>
                </v-flex>

                <v-flex>
                  <v-checkbox v-model="editedItem.subbed_due_to_injury" label="Subbed due to injury"></v-checkbox>
                </v-flex>

                <v-flex>
                  <v-checkbox v-model="editedItem.yellow_cards" label="Yellow Card"></v-checkbox>
                </v-flex>

                <v-flex>
                  <v-checkbox v-model="editedItem.red_cards" label="Red Card"></v-checkbox>
                </v-flex>
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

    <v-data-table v-if="Array.isArray(this.player_matches)"
      :headers="headers"
      :items="player_matches"
      hide-actions
      class="elevation-1"
    >
      <template slot="items" slot-scope="props">
        <td>{{ props.item.player_label }}</td>
        <td><v-icon v-show="props.item.starter">done</v-icon></td>
        <td>{{ props.item.minutes }}</td>
        <td>{{ props.item.corners }}</td>
        <td><v-icon v-show="props.item.subbed_due_to_injury">done</v-icon></td>
        <td><v-icon v-show="props.item.yellow_cards">done</v-icon></td>
        <td><v-icon v-show="props.item.red_cards">done</v-icon></td>

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
    <v-btn @click="backToMatch()" color="error">Back To Match</v-btn>
  </div>
</template>

<script>
import API from '@/lib/API'

export default {
  props: ['player_matches', 'onSubmit', 'onCancel'],
  data: () => ({
    dialog: false,
    players: [],
    headers: [
      {
        text: 'Player',
        value: 'player'
      },
      {
        text: 'Starter',
        value: 'starter'
      },
      {
        text: 'Minutes',
        value: 'minutes'
      },
      {
        text: 'Corners',
        value: 'corners'
      },
      {
        text: 'Subbed to to injury',
        value: 'subbed_due_to_injury'
      },
      {
        text: 'Yellow Cards',
        value: 'yellow_cards'
      },
      {
        text: 'Red Cards',
        value: 'red_cards'
      },
      {
        text: 'Actions',
        value: 'actions'
      }

    ],
    editedIndex: -1,
    editedItem: {
      player_label: ''
    },
    defaultItem: {
      player_label: '',
      player_id: null,
      corners: 0,
      minutes: null,
      starter: false,
      subbed_due_to_injury: false,
      yellow_cards: false,
      red_cards: false
    },
    valid: true
  }),
  //created () {
  //    this.initialize()
  //},
  computed: {
    formTitle () {
      return this.editedIndex === -1 ? 'New Player Match' : 'Edit Player Match'
    },
  },
  watch: {
    dialog (val) {
      val || this.close()
    }
  },
  mounted () {
    // TODO : move into store
    API.getPlayers()
      .then(players => {
        this.players = players
      })
  },
  methods: {
    submit () {
      if (this.valid) {
        this.onSubmit()
      }
    },
    cancel () {
      this.onCancel()
    },
    editItem (item) {
      this.editedIndex = this.player_matches.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialog = true
    },
    deleteItem (item) {
      const index = this.player_matches.indexOf(item)

      if (confirm('Are you sure you want to delete this item?') && this.player_matches.splice(index, 1)) {
        API.deletePlayerMatch(item.id)
      }
    },
    close () {
      this.dialog = false
      setTimeout(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      }, 300)
    },
    initialize () {
      alert("not imple yo!")
    },
    save () {
      if (this.editedIndex > -1) {
        // updated existing PlayerMatch
        Object.assign(this.player_matches[this.editedIndex], this.editedItem)
        API.updatePlayerMatch(this.editedItem.id, this.editedItem)
      } else {
        // create new  PlayerMatch
        const match_id = this.$route.params.id
        this.editedItem.match = match_id
        API.createPlayerMatch(this.editedItem)
        .then((player_match) => {
          this.player_matches.push(player_match)
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
