<template id="competition-props">
    <div>
        <div class="form-group">
            <label for="edit-name">Name</label>
            <input class="form-control" id="edit-name" v-model="competition.name" required/>

            <label for="edit-result">Result</label>
            <input class="form-control" id="edit-result" v-model="competition.result"/>

            <label for="edit-url">Competition's website</label>
            <input type="url" class="form-control" id="edit-url" v-model="competition.external_url"/>
        </div>
    </div>
</template>

<script>

export default {
    props: ['competition'],
    data () {
        return {};
    }
}
</script>