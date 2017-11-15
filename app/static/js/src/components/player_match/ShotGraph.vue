<template id="shot-graph">
    <div class="container">
        <h2 id="section">Shot data</h2>

        <div class="row">
            <div class="col-sm-6" id="convas-container">
                <canvas id="canvas" width=350 height=260></canvas>
                <p id="sub-table-note">
                    <i>Grey: not on goal, Blue: on goal, Red: scored.</i>
                </p>
            </div>

            <div class="col-sm-6">
                <div class="cliente">

                    <h4 style="text-decoration: underline">Shot details</h4>
                    <div v-if="selectedShot">
                        <form class="form-horizontal">

                            <div class="form-group">
                                <label for="shotPlayer"
                                       class="col-sm-4 control-label">Player :
                                </label>
                                <div class="col-sm-8">
                                    <input type="text"
                                           class="form-control"
                                           id="shotPlayer"
                                           v-model="selectedShot.player_match.player.name"
                                           :disabled="enableEditing == 0">
                                </div>
                            </div>

                            <div class="form-group">
                                <label for="shotOnGoal"
                                       class="col-sm-4 control-label">On Goal :
                                </label>
                                <div class="col-sm-2">
                                    <input type="checkbox"
                                           class="form-control"
                                           id="shotOnGoal"
                                           v-model="selectedShot.on_goal"
                                           :disabled="enableEditing == 0">
                                </div>
                                <label for="shotScored"
                                       class="col-sm-3 control-label">Scored :
                                </label>
                                <div class="col-sm-3">
                                    <input type="checkbox"
                                           class="form-control"
                                           id="shotScored"
                                           v-on:click="toggleShotScored"
                                           v-model="selectedShot.scored"
                                           :disabled="enableEditing == 0">
                                </div>
                            </div>

                            <div class="form-group">
                                <label for="shotIsPk"
                                       class="col-sm-4 control-label">Penalty Kick :
                                </label>
                                <div class="col-sm-2">
                                    <input type="checkbox"
                                           class="form-control"
                                           id="shotIsPk"
                                           v-model="selectedShot.pk"
                                           :disabled="enableEditing == 0">
                                </div>
                                <div class="col-sm-6"></div>
                            </div>


                            <div v-if="selectedShot.goal">
                                <h4 style="text-decoration: underline">Goal info</h4>

                                <div class="form-group" >
                                    <label for="goalTime"
                                           class="col-sm-4 control-label">Time :
                                    </label>
                                    <div class="col-sm-8">
                                        <input type="number disabled"
                                               class="form-control"
                                               id="goalTime"
                                               v-model="selectedShot.goal.time"
                                               :disabled="enableEditing == 0">
                                    </div>
                                </div>

                                <div class="form-group" v-if="selectedShot.goal.assist">
                                    <label for="shotScored"
                                           class="col-sm-4 control-label">Assist :
                                    </label>
                                    <div class="col-sm-8">
                                        <input type="text"
                                               class="form-control"
                                               id="shotScored"
                                               v-model="selectedShot.goal.assist.player_match.player.name"
                                               :disabled="enableEditing == 0">
                                    </div>
                                </div>
                            </div>
                        </form>

                        <div v-if="enableEditing">
                            <a class="btn btn-default" v-on:click="saveShotEdits">Save</a>
                            <a class="btn btn-default" v-on:click="deleteShot">Delete</a>
                        </div>
                    </div>
                    <div v-else>
                            Click on existing shot to modify it<br/> or <br/>
                            <a class="btn btn-default" v-on:click="newShot">Add a Shot</a><br/>
                    </div>

                </div>
            </div>
        </div>
    </div>
</template>

<script>

import axios from 'axios'
import { fabric } from 'fabric'
import _ from 'lodash'


export default {
    props: {enableEditing: {default: false}
    },
    data () {
        return {
            shots: [],
            circles: [],
            canvas: null,
            selectedShot: "",
            selectedShotIsModified: false}
    },
    ready (){
        console.log("READY");
    },
    created() {
        var parent = this;
        axios.get(`/api/v1/shots/?match_id=` + this.$route.params.match_id + `&by_opponent=false&expand=true`)
        .then(response => {
            this.shots = response.data;

            this.drawShotsOnCanvas()
        })
    },
    mounted() {
        console.log("MOUNTED");
        var parent = this;
        var canvas = new fabric.Canvas('canvas');

        canvas.selection = false; // disable group selection
        canvas.on('mouse:down', function(options) {
            if (options.target) {
                console.log('Shot clicked ');
                console.log(' - id     : ' + options.target.shot.id);
                console.log(' - player : ' + options.target.shot.player_match.player.name);
                console.log(' - scored : ' + options.target.shot.scored);
                parent.selectedShot = options.target.shot.id;
                parent.selectedShot = JSON.parse(JSON.stringify(options.target.shot));

            }
            else {
                console.log('blanky');
                parent.selectedShot = "";
            }
        });
        //canvas.renderAll()
        this.canvas = canvas

    },
    computed: {
        selectedShotData: function () {
            return _.find(this.shots, {id: this.selectedShot})
        }

    },
    methods: {
        drawShotsOnCanvas: function(event){
            console.log("inside drawShotsOnCanvas!")
            var parent = this;
            var canvas = this.canvas; // keeps adding to same canvas

            //canvas = new fabric.Canvas('canvas');
            canvas.clear()
            console.log("inside drawShotsOnCanvas 2!")
            console.log(this.shots.length)
            var iii = 0;
            for (iii = 0; iii < this.shots.length; iii++) {
                var shot = this.shots[iii];
                var color = 'black';
                if (shot.scored) {
                    color = 'rgb(250,15,15)'; //red
                } else if (shot.on_goal) {
                    color = 'rgb(15,100,200)'; //blue
                } else {
                    color = 'grey'; //grey
                }

                var circle = new fabric.Circle({
                                    radius: 7,
                                    fill: color,
                                    opacity: 0.9,
                                    stroke: 'rgb(10,10,10)',
                                    strokeWidth: 2,
                                    originX: 'center',
                                    originY: 'center',
                                    lockMovementX: this.enableEditing == false,
                                    lockMovementY: this.enableEditing == false
                                    })

                //
                var text = new fabric.Text(shot.player_match.player.number.toString(),
                                           {fontSize: 10,
                                            originX: 'center',
                                            originY: 'center'
                                           }
                );

                var group = new fabric.Group([circle, text],
                                             {hasControls: false,
                                              left: shot.x,
                                              top: shot.y,
                                              angle: 0
                                              }
                );

                group.toObject = (function(toObject) {
                  return function() {
                    return fabric.util.object.extend(toObject.call(this), {
                      shot: this.shot
                    });
                  };
                })(group.toObject);
                group.shot = shot

                group.on('modified', function(){
                    //console.log('moved ' + this.shot.player_match.player.name + '(' + this.left + ', ' + this.top + ')')
                    parent.selectedShot.x = this.left;
                    parent.selectedShot.y = this.top;
                    parent.selectedShotIsModified = true;
                })

                canvas.add(group)
            }
            canvas.setBackgroundImage("static/assets/soccer-pitch.png",
                                      canvas.renderAll.bind(canvas),
                                      {backgroundImageOpacity: 0.5,
                                       backgroundImageStretch: false
                                      }
            );
            //canvas.renderAll()
        },
        toggleShotScored: function(e){


            if ((e.target.checked == true) &
               (_.has(this.selectedShot.goal, 'id') == false)) {
                console.log("OK1")
                axios.post(`/api/v1/goals/`, {shot: this.selectedShot})
                .then(response => {
                    this.data = response.data;
                    console.log("ADDED GOAL")
                })
                .catch(e => {
                    console.log(e)
                })
                console.log("OK2")
            } else {
                console.log("REMOVE GOAL")
            };
            console.log("OK3")


        },
        refreshCanvas: function (event) {
            console.log("REFRESH CANVAS")
        },
        saveShotEdits: function (event) {
            console.log(this.selectedShot);

            // capture player_match since patch returns non-expanded
            var pm = this.selectedShot.player_match;
            axios.patch(this.selectedShot._links.self,
                        {x: this.selectedShot.x,
                         y: this.selectedShot.y,
                         on_goal: this.selectedShot.on_goal,
                         scored: this.selectedShot.scored,
                         pk: this.selectedShot.pk,
                         by_opponent: this.selectedShot.by_opponent
                        }
            )
            .then(response => {
                console.log("UPDATE shot successful!")
                var shot = response.data;
                shot['player_match'] = pm;
                var index = _.findIndex(this.shots, {id: shot.id})
                this.shots.splice(index, 1, shot)
                this.drawShotsOnCanvas()
            })
            .catch(e => {
                alert("UPDATE shot failed")
                console.log(e)
            })

        },
        deleteShot: function (event) {

            // capture the seleected shot info
            var selectedShotUri = this.selectedShot._links.self
            var selectedShotId = this.selectedShot.id

            // clear it so control goes back to default mode
            this.selectedShot = ""

            // delete the shot
            axios.delete(selectedShotUri)
            .then(response => {
                console.log("DELETE shot successful!")
                //this.$router.go(-1)
            })
            .catch(e => {
                alert("DELETE shot failed")
                console.log(e)
            })
            _.remove(this.shots, {id: selectedShotId})
            this.drawShotsOnCanvas()
        },
        newShot: function (event) {
            alert("newShot");
            this.drawShotsOnCanvas()
        },
        highlightShot: function (event) {
            //http://fabricjs.com/docs/fabric.Circle.html
            //circle.bringToFront
            //circle.transform(

        }
    }
}

</script>


<style>

#canvas {
    padding: 0;
    margin: auto;
    display: block;
    width: 500px;
}

.cliente {
	margin-top:10px;
	border: #cdcdcd medium solid;
	border-radius: 10px;
	-moz-border-radius: 10px;
	-webkit-border-radius: 10px;
}

</style>