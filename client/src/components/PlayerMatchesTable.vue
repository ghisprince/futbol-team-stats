<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="player_matches"
      :pagination.sync="showPlayer ? undefined : pagination"
      :loading="true"
    >
      <v-progress-linear v-show="showProgress"
                         slot="progress"
                         color="blue"
                         indeterminate>
      </v-progress-linear>
      <template slot="headerCell" slot-scope="props">
        <v-tooltip bottom>
          <span slot="activator">
            {{ props.header.text }}
          </span>
          <span>
            {{ props.header.tooltip ? props.header.tooltip : props.header.text  }}
          </span>
        </v-tooltip>
      </template>

      <template slot="items" slot-scope="props">
        <td v-if="showPlayer">
            <router-link :to="{
              name: 'Player',
              params: { id: props.item.player }
            }">
            {{ props.item.player_label }}
          </router-link>
        </td>
        <td v-if="showMatch">{{ props.item.match.date_time | formatDate }}</td>
        <td v-if="showMatch">
            <router-link :to="{
              name: 'Competition',
              params: { id: props.item.match.competition_id }
            }">
            {{ props.item.match.competition_name }}
          </router-link>
        </td>
        <td v-if="showMatch">
            <router-link :to="{
              name: 'Opponent',
              params: { id: props.item.match.opponent_id }
            }">
            {{ props.item.match.opponent_name }}
          </router-link>
        </td>
        <td><v-icon v-show="props.item.starter">done</v-icon></td>
        <td><span v-show="props.item.minutes">{{ props.item.minutes }}</span></td>
        <td><span v-show="props.item.num_goals > 0">{{ props.item.num_goals }}</span></td>
        <td><span v-show="props.item.num_assists > 0">{{ props.item.num_assists }}</span></td>
        <td><span v-show="props.item.num_shots > 0">{{ props.item.num_shots }}</span></td>
        <td><span v-show="props.item.corners > 0">{{ props.item.corners }}</span></td>
        <td><span v-show="props.item.yellow_cards > 0">{{ props.item.yellow_cards }}</span></td>
        <td><span v-show="props.item.red_cards > 0">{{ props.item.red_cards }}</span></td>
        <td><v-icon v-show="props.item.subbed_due_to_injury">done</v-icon></td>

        <td v-if="showMatch">
            <router-link :to="{
              name: 'Match',
              params: { id: props.item.match.id }
            }">
            <v-icon>insert_chart</v-icon>
          </router-link>
        </td>

      </template>

      <template slot="footer">
        <td v-if="showPlayer"><strong>Players: {{ player_matches.length }} </strong></td>
        <td v-if="showMatch">Matches: {{ player_matches.length }} </td>
        <td v-if="showMatch">-</td>
        <td v-if="showMatch">-</td>

        <td><strong> {{ sum_starters }} </strong></td>
        <td><strong> {{ sum_minutes }} </strong></td>
        <td><strong> {{ sum_goals }} </strong></td>
        <td><strong> {{ sum_assist }} </strong></td>
        <td><strong> {{ sum_shots }} </strong></td>
        <td><strong> {{ sum_corners }} </strong></td>
        <td><strong> {{ sum_yellow_cards }} </strong></td>
        <td><strong> {{ sum_red_cards }} </strong></td>
        <td><strong> {{ sum_subbed_due_to_injury }} </strong></td>
        <td v-if="showMatch">-</td>
      </template>
    </v-data-table>
  </div>
</template>

<script>
import UTILS from '@/lib/UTILS'

export default {
  props: ['player_matches', 'showMatch', 'showPlayer', 'showProgress'],
  data () {
    return {
      pagination: {
        sortBy: 'match.date_time',
        descending: true
      }
    }
  },
  computed: {
    headers: function () {
      let arr = []
      if (this.showPlayer) {
        arr.push({ text: 'Player', value: 'player_label' })
      }
      if (this.showMatch) {
        arr.push({ text: 'Date', value: 'match.date_time' })
      }
      if (this.showMatch) {
        arr.push({ text: 'Competition', value: 'match.competition_name', sortable: false })
      }
      if (this.showMatch) {
        arr.push({ text: 'Opponent', value: 'match.opponent_name' })
      }
      arr.push.apply(arr, [
        { text: 'Starter', tooltip: 'In starting 11', value: 'starter' },
        { text: 'Min', tooltip: 'Minutes played', value: 'minutes' },
        { text: 'Goals', value: 'num_goals' },
        { text: 'Assists', value: 'num_assists' },
        { text: 'Shots', tooltip: 'Attempts on goal', value: 'num_shots' },
        { text: 'Corners', value: 'corners' },
        { text: 'YC', tooltip: 'Yellow Cards', value: 'yellow_cards' },
        { text: 'RC', tooltip: 'Red Cards', value: 'red_cards' },
        { text: 'Injury', tooltip: 'Subsituted due to injury', value: 'subbed_due_to_injury' }
      ])
      if (this.showMatch) {
        arr.push({ text: 'Match Details', value: 'match.id' })
      }
      return arr
    },
    sum_starters: function () {
      return UTILS.sum(this.player_matches, 'starter')
    },
    sum_minutes: function () {
      return UTILS.sum(this.player_matches, 'minutes')
    },
    sum_goals: function () {
      return UTILS.sum(this.player_matches, 'num_goals')
    },
    sum_assist: function () {
      return UTILS.sum(this.player_matches, 'num_assists')
    },
    sum_shots: function () {
      return UTILS.sum(this.player_matches, 'num_shots')
    },
    sum_corners: function () {
      return UTILS.sum(this.player_matches, 'corners')
    },
    sum_yellow_cards: function () {
      return UTILS.sum(this.player_matches, 'yellow_cards')
    },
    sum_red_cards: function () {
      return UTILS.sum(this.player_matches, 'red_cards')
    },
    sum_subbed_due_to_injury: function () {
      return UTILS.sum(this.player_matches, 'subbed_due_to_injury')
    }
  }
}

</script>
