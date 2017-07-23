<template id="opponent-edit">
    <div>
        <div class="form-group">
            <label for="edit-name">Name</label>
            <input class="form-control" id="edit-name" v-model="opponent.name" required/>

            <label for="edit-url">URL</label>
            <input type="url"  class="form-control" id="edit-url" v-model="opponent.external_url"/>
        </div>
    </div>
</template>


<script>

export default {
    props: ['opponent'],
    data () {
        return {};
    }
}
</script>