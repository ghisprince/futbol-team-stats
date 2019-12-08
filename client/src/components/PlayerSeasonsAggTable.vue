<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="agg_player_matches"
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
              params: { id: props.item.player_id }
            }">
            {{ props.item.player_label }}
          </router-link>
        </td>

        <td v-if="showSeason">
            <router-link :to="{
              name: 'Season',
              params: { id: props.item.season_id }
            }">
            {{ props.item.season_name }}
          </router-link>
        </td>

        <td>{{ props.item.apps }} (of {{ props.item.matches }})</td>
        <td><span v-show="props.item.minutes">{{ props.item.minutes }}</span></td>
        <!-- <td><span v-show="props.item.minutes_avr">{{ props.item.minutes_avr }}</span></td> -->
        <td><span v-show="props.item.goals > 0">{{ props.item.goals }}</span></td>
        <td><span v-show="props.item.assists > 0">{{ props.item.assists }}</span></td>
        <td><span v-show="props.item.shots > 0">{{ props.item.shots }}</span></td>
        <td><span v-show="props.item.yellow_cards > 0">{{ props.item.yellow_cards }}</span></td>
        <td><span v-show="props.item.red_cards > 0">{{ props.item.red_cards }}</span></td>
        <td><span v-show="props.item.subbed_due_to_injury">{{ props.item.subbed_due_to_injury }}</span></td>
      </template>

      <template slot="footer">
        <td v-if="showPlayer"><strong>Players: {{ agg_player_matches.length }} </strong></td>
        <td v-if="showSeason"><strong>Seasons:  {{ agg_player_matches.length }} </strong></td>
        <td v-if="!showPlayer"><strong> {{ sum_apps }} (of {{ sum_matches }}) </strong></td>
        <td v-else>-</td>
        <td><strong> {{ sum_minutes }} </strong></td>
        <!-- <td><strong>  </strong></td> minutes_avr -->
        <td><strong> {{ sum_goals }} </strong></td>
        <td><strong> {{ sum_assist }} </strong></td>
        <td><strong> {{ sum_shots }} </strong></td>
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
  props: ['agg_player_matches', 'showPlayer', 'showSeason', 'showProgress'],
  data () {
    return {
      pagination: {
        sortBy: 'season_name',
        descending: true,
        rowsPerPage: -1
      }
    }
  },
  computed: {
    headers: function () {
      let arr = []
      if (this.showPlayer) {
        arr.push({ text: 'Player', value: 'player_label' })
      }
      if (this.showSeason) {
        arr.push({ text: 'Season', value: 'season_name' })
      }
      arr.push.apply(arr, [
        { text: 'Apps', tooltip: 'Appearances', value: 'apps' },
        { text: 'Min', tooltip: 'Minutes played', value: 'minutes' },
        // { text: 'Min per App', tooltip: 'Minutes played per appearance', value: 'minutes_avr' },
        { text: 'Goals', tooltip: 'Goals Scored', value: 'goals' },
        { text: 'Assists', tooltip: 'Goals Assisted', value: 'assists' },
        { text: 'Shots', tooltip: 'Attempts on goal', value: 'shots' },
        { text: 'YC', tooltip: 'Yellow Cards', value: 'yellow_cards' },
        { text: 'RC', tooltip: 'Red Cards', value: 'red_cards' },
        { text: 'Injury',
          tooltip: 'Number Of Times Subsituted due to injury',
          value: 'subbed_due_to_injury' }
      ])

      return arr
    },
    sum_apps: function () {
      return UTILS.sum(this.agg_player_matches, 'apps')
    },
    sum_matches: function () {
      return UTILS.sum(this.agg_player_matches, 'matches')
    },
    sum_minutes: function () {
      return UTILS.sum(this.agg_player_matches, 'minutes')
    },
    sum_goals: function () {
      return UTILS.sum(this.agg_player_matches, 'goals')
    },
    sum_assist: function () {
      return UTILS.sum(this.agg_player_matches, 'assists')
    },
    sum_shots: function () {
      return UTILS.sum(this.agg_player_matches, 'shots')
    },
    sum_yellow_cards: function () {
      return UTILS.sum(this.agg_player_matches, 'yellow_cards')
    },
    sum_red_cards: function () {
      return UTILS.sum(this.agg_player_matches, 'red_cards')
    },
    sum_subbed_due_to_injury: function () {
      return UTILS.sum(this.agg_player_matches, 'subbed_due_to_injury')
    }
  }
}

</script>
