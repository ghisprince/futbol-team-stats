<template id="edit-choices">
    <div id="edit-choices-style">
        <h1>What do you wish to edit?</h1>
        <ul>
            <li>
                <router-link v-bind:to="'opponent-list'">Matches</router-link>
            </li>
            <li>
                <router-link v-bind:to="'opponent-list'">Opponents</router-link>
            </li>
            <li>
                <router-link v-bind:to="'opponent-list'">Players</router-link>
            </li>
            <li>
                <router-link v-bind:to="'competition-list'">Competitions</router-link>
            </li>
            <li>
                <router-link v-bind:to="'opponent-list'">Team</router-link>
            </li>
        </ul>
    </div>
</template>


<script>
import axios from 'axios'
import _ from 'lodash'

export default {
    data () {
        return {}
    },
    created() {},
    computed: {}
}
</script>


<style>
li {
    text-align: left;
}
</style>