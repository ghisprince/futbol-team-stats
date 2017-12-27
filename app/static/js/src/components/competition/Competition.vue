<template id="competition-props">
    <div class="container-fluid">

        <div class="form-group row">
            <div class="col-sm-2"/>
            <label for="edit-name" class="col-sm-3 col-form-label">Name</label>
            <div class="col-sm-4">
                <input class="form-control" id="edit-name" v-model="competition.name" required/>
            </div>
        </div>

        <div class="form-group row">
            <div class="col-sm-2"/>
            <label for="edit-result" class="col-sm-3 col-form-label">Result</label>
            <div class="col-sm-4">
                <input class="form-control" id="edit-result" v-model="competition.result"/>
            </div>
        </div>

        <div class="form-group row">
            <div class="col-sm-2"/>
            <label for="edit-url" class="col-sm-3 col-form-label">Competition's website</label>
            <div class="col-sm-4">
                <input type="url" class="form-control" id="edit-url" v-model="competition.external_url"/>
            </div>
        </div>

        <div class="form-group row">
            <div class="col-sm-2"/>
            <label for="edit-note" class="col-sm-3 col-form-label">Note</label>
            <div class="col-sm-4">
                <input class="form-control" id="edit-note" v-model="competition.note"/>
            </div>
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