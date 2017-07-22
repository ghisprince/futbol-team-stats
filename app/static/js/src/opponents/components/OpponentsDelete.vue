<template id="opponent-delete">
    <div>
        <h2>Delete opponent : {{ opponent.name }}</h2>
        <form v-on:submit="deleteOpponent">
            <p>The action cannot be undone.</p>
            <button type="submit" class="btn btn-danger">Delete</button>
            <router-link class="btn btn-default" v-bind:to="'/'">Cancel</router-link>
        </form>

        <div v-if="showAlert"> <!-- hack due to https://github.com/vuejs/vue-router/issues/252 -->
            <alert :show='true' placement="top" :duration="5" type="danger" width="400px" dismissable>
                <span class="icon-info-circled alert-icon-float-left"></span>
                <strong>ERROR!</strong>
                <p>{{alertMessage}}</p>
            </alert>
        </div>
    </div>
</template>


<script>
import axios from 'axios'
import alert from 'vue-strap/src/alert.vue'

export default {
    data () {
        return {opponent: {name: ''},
                showAlert: false,
                alertMessage: "aaa" }
    },
    components: {alert: alert},
    created() {
        axios.get(`/api/v1/opponents/` + this.$route.params.opponent_id)
        .then(response => {
            this.opponent = response.data
        })
        .catch(e => {
            console.log(e)
        })
    },

    methods: {
        deleteOpponent: function() {
            axios.delete(this.opponent._links.self)

            .then(response => {
                this.$router.push('/')
            })
            .catch(e => {
                this.alertMessage = e.response.data.error;
                this.showAlert = true;

            })
        }
    }
}

</script>