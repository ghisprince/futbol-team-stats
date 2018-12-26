<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="aggregatePMs"
      :pagination.sync="showPlayer ? undefined : pagination"
      :loading="true"
    >
      <v-progress-linear v-show="showProgress" slot="progress" color="blue" indeterminate></v-progress-linear>
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
              params: { id: props.item.player_id }
            }">
            {{ props.item.player_label }}
          </router-link>
        </td>

        <td v-if="showCompetition">
            <router-link :to="{
              name: 'Competition',
              params: { id: props.item.competition_id }
            }">
            {{ props.item.id }}
          </router-link>
        </td>
        <td>{{ props.item.apps }}</td>
        <td>{{ props.item.starter }}</td>
        <td><span v-show="props.item.minutes">{{ props.item.minutes }}</span></td>
        <td><span v-show="props.item.num_goals > 0">{{ props.item.num_goals }}</span></td>
        <td><span v-show="props.item.num_assists > 0">{{ props.item.num_assists }}</span></td>
        <td><span v-show="props.item.num_shots > 0">{{ props.item.num_shots }}</span></td>
        <td><span v-show="props.item.corners > 0">{{ props.item.corners }}</span></td>
        <td><span v-show="props.item.yellow_cards > 0">{{ props.item.yellow_cards }}</span></td>
        <td><span v-show="props.item.red_cards > 0">{{ props.item.red_cards }}</span></td>
        <td><span v-show="props.item.subbed_due_to_injury">{{ props.item.subbed_due_to_injury }}</span></td>
      </template>

      <template slot="footer">
        <td v-if="showPlayer"><strong>Players: {{ aggregatePMs.length }} </strong></td>
        <td v-if="showCompetition"><strong>Competitions:  {{ aggregatePMs.length }} </strong></td>
        <td v-if="!showPlayer"><strong> {{ sum_apps }} </strong></td>
        <td v-else>-</td>
        <td v-if="!showPlayer"><strong> {{ sum_starters }} </strong></td>
        <td v-else>-</td>
        <td><strong> {{ sum_minutes }} </strong></td>
        <td><strong> {{ sum_goals }} </strong></td>
        <td><strong> {{ sum_assist }} </strong></td>
        <td><strong> {{ sum_shots }} </strong></td>
        <td><strong> {{ sum_corners }} </strong></td>
        <td><strong> {{ sum_yellow_cards }} </strong></td>
        <td><strong> {{ sum_red_cards }} </strong></td>
        <td><strong> {{ sum_subbed_due_to_injury }} </strong></td>
      </template>
    </v-data-table>
  </div>
</template>

<script>
import UTILS from '@/lib/UTILS'

export default {
  props: ['player_matches', 'showPlayer', 'showCompetition'],
  data () {
    return {
      pagination: {
        sortBy: 'date_time',
        descending: true
      }
    }
  },
  updated () {
  },
  computed: {
    showProgress: function () {
      return this.player_matches.length === 0
    },
    headers: function () {
      let arr = []
      if (this.showPlayer) {
        arr.push({ text: 'Player', value: 'player_label' })
      }
      if (this.showCompetition) {
        arr.push({ text: 'Competition', value: 'date_time' })
      }
      arr.push.apply(arr, [
        { text: 'Apps', tooltip: 'Appearances', value: 'apps' },
        { text: 'Starter', tooltip: 'In starting lineup', value: 'starter' },
        { text: 'Min', tooltip: 'Minutes played', value: 'minutes' },
        { text: 'Goals', tooltip: 'Goals Scored', value: 'num_goals' },
        { text: 'Assists', tooltip: 'Goals Assisted', value: 'num_assists' },
        { text: 'Shots', tooltip: 'Attempts on goal', value: 'num_shots' },
        { text: 'Corners', tooltip: 'Corners taken', value: 'corners' },
        { text: 'YC', tooltip: 'Yellow Cards', value: 'yellow_cards' },
        { text: 'RC', tooltip: 'Red Cards', value: 'red_cards' },
        { text: 'Injury', tooltip: 'Number Of Times Subsituted due to injury', value: 'subbed_due_to_injury' }
      ])

      return arr
    },
    aggregatePMs: function () {
      if (this.showPlayer) {
        return UTILS.aggregateByPlayer(this.player_matches)
      } else {
        return UTILS.aggregateByCompetition(this.player_matches)
      }
    },
    sum_apps: function () {
      return (this.player_matches.length)
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
