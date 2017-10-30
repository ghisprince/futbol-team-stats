<template id="opponent-edit">
    <div class="container-fluid">

        <div class="form-group row">
            <div class="col-sm-2"/>
            <label for="edit-name" class="col-sm-3 col-form-label">Name</label>
            <div class="col-sm-4">

                <input class="form-control" id="edit-name" v-model="opponent.name" required/>
            </div>
        </div>

        <div class="form-group row">
            <div class="col-sm-2"/>
            <label for="edit-url" class="col-sm-3 col-form-label">URL</label>
            <div class="col-sm-4">

                <input type="url"  class="form-control" id="edit-url" v-model="opponent.external_url"/>
            </div>
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