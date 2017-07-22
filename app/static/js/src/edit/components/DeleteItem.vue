<template id="opponent-delete">
    <div>
        <h2>Delete {{ type }} '{{ name }}'</h2>
        <div>
            <p>The action cannot be undone.</p>
            <button class="btn btn-danger" v-on:click="deleteOpponent">Delete</button>
            <button class="btn btn-default" v-on:click="goBack">Cancel</button>
        </div>

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
    props: ['name', 'uri', 'type', 'canDelete'],
    data () {
        return {showAlert: false,
                alertMessage: ""
                }
    },
    components: {alert: alert},
    created() {},
    methods: {
        goBack: function() {
            this.$router.go(-1)
        },
        deleteOpponent: function() {
            axios.delete(this.uri)

            .then(response => {
                this.$router.go(-1)
            })
            .catch(e => {
                this.alertMessage = e.response.data.error;
                this.showAlert = true;
            })
        }
    }
}

</script>