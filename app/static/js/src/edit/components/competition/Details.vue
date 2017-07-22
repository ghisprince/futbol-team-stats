<template id="competition">
    <div>
        <h2>{{ competition.name }}</h2>

        <a v-bind:href="competition.external_url">Competition's web site</a>

        <p>Below are the team's results in this competition </p>
        <table class="table">
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Opponent</th>
                    <th>Result</th>
                    <th>Goals</th>
                    <th>Goals against</th>
                    <th>Shots</th>
                    <th>Shots against</th>
                    <th>Match details</th>
                </tr>
            </thead>
            <tfoot>
                <tr>
                    <td>-</td>
                    <td>-</td>
                    <td>-</td>
                    <td>-</td>
                    <td>-</td>
                    <td>-</td>
                    <td>99</td>
                    <td>-</td>
                </tr>
            </tfoot>
            <tbody>
                <tr v-for="match in orderedMatches">
                    <td>
                        {{ match.date_time | formatDate }}
                    </td>
                    <td>
                        {{ match.opponent.name }}
                    </td>
                    <td>
                        {{ match.result }}
                    </td>
                    <td>
                        {{ match.num_goals }}
                    </td>
                    <td>
                        {{ match.num_goals_against }}
                    </td>
                    <td>
                        {{ match.num_shots }}
                    </td>
                    <td>
                        {{ match.num_shots_against }}
                    </td>
                    <td>
                        -link-
                    </td>
                </tr>
            </tbody>
        </table>
        <span class="glyphicon glyphicon-arrow-left" aria-hidden="true"></span>
        <router-link v-bind:to="'/competition-list'">Back to competition list</router-link>
    </div>
</template>


<script>
import axios from 'axios'
import _ from 'lodash'

export default {
    props: ['uri'],
    data () {
        return {competition: {name: ''},
                competition_external_url_mock: "https://home.gotsoccer.com/rankings/event.aspx?EventID=54275&GroupID=643091"
                }
    },
    created() {
        // get competition data
        axios.get(this.uri + `?expand=true`)
        .then(response => {
            this.competition = response.data
        })
    },
    computed: {
        orderedMatches: function() {
            return _.orderBy(this.competition.matches, 'date_time', 'desc')
        }
    }
}

</script>

<style>
</style>