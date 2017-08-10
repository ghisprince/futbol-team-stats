<template id="shot-graph">
    <div class="container">
        <h2 id="section">Shot data</h2>

        <div class="row">
            <div class="col-sm-7" id="convas-container">
                <canvas id="canvas" width=500 height=400  ></canvas>
                <p id="sub-table-note"><i>Red: scored, Blue: on goal, Grey: not on goal.</i></p>
            </div>

            <div class="col-sm-5">
                <div class="cliente">

                    <h4 style="text-decoration: underline">Shot details</h4>
                    <div v-if="selectedShot">
                        <form class="form-horizontal">

                            <div class="form-group">
                                <label for="shotPlayer" class="col-sm-4 control-label">Player :</label>
                                <div class="col-sm-8">
                                    <input type="text" class="form-control" id="shotPlayer" v-model="selectedShot.player_match.player.name" :disabled="enableEditing == 0">
                                </div>
                            </div>

                            <div class="form-group">
                                <label for="shotOnGoal" class="col-sm-4 control-label">On Goal :</label>
                                <div class="col-sm-2">
                                    <input type="checkbox" class="form-control" id="shotOnGoal" v-model="selectedShot.on_goal" :disabled="enableEditing == 0">
                                </div>
                                <label for="shotScored" class="col-sm-3 control-label">Scored :</label>
                                <div class="col-sm-3">
                                    <input type="checkbox" class="form-control" id="shotScored" v-model="selectedShot.scored" :disabled="enableEditing == 0">
                                </div>
                            </div>

                            <div class="form-group">
                                <label for="shotIsPk" class="col-sm-4 control-label">Penalty Kick :</label>
                                <div class="col-sm-2">
                                    <input type="checkbox" class="form-control" id="shotIsPk" v-model="selectedShot.pk" :disabled="enableEditing == 0">
                                </div>
                                <div class="col-sm-6"></div>
                            </div>


                            <div v-if="selectedShot.goal">
                                <h4 style="text-decoration: underline">Goal info</h4>

                                <div class="form-group" >
                                    <label for="goalTime" class="col-sm-4 control-label">Time :</label>
                                    <div class="col-sm-8">
                                        <input type="number disabled" class="form-control" id="goalTime" v-model="selectedShot.goal.time" :disabled="enableEditing == 0">
                                    </div>
                                </div>

                                <div class="form-group" v-if="selectedShot.goal.assist">
                                    <label for="shotScored" class="col-sm-4 control-label">Assist :</label>
                                    <div class="col-sm-8">
                                        <input type="text" class="form-control" id="shotScored" v-model="selectedShot.goal.assist.player_match.player.name" :disabled="enableEditing == 0">
                                    </div>
                                </div>
                            </div>
                        </form>

                        <div v-if="enableEditing">
                            <button v-on:click="refreshCanvas">Save changes!</button>
                            <button v-on:click="refreshCanvas">Delete!</button>
                        </div>
                    </div>
                    <div v-else>
                        click yo!
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
    props: [],
    data () {
        return {
            shots: [],
            circles: [],
            canvas: null,
            selectedShot: "",
            enableEditing: false
               }
    },
    ready (){
        console.log("READY");
    },
    created() {
        var parent = this;
        axios.get(`http://127.0.0.1:5000/api/v1/shots/?match_id=` + this.$route.params.match_id + `&expand=true`)
        .then(response => {
            var shots = response.data;
            this.shots = shots

            var canvas = this.canvas; // keeps adding to same canvas
            //canvas = new fabric.Canvas('canvas');
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
                                     });

                var group = new fabric.Group([ circle, text], {
                                    hasControls: false,
                                    left: shot.x * 10,
                                    top: shot.y * 10,
                                    angle: 0
                                    });

                group.toObject = (function(toObject) {
                  return function() {
                    return fabric.util.object.extend(toObject.call(this), {
                      shot: this.shot
                    });
                  };
                })(group.toObject);
                group.shot = shot

                group.on('modified', function(){
                    console.log('moved ' + this.shot.player_match.player.name + '(' + this.left + ', ' + this.top + ')')
                })

                canvas.add(group)
            }

            this.canvas.renderAll()
        })
    },
    mounted() {
        console.log("MOUNTED");
        var canvas = new fabric.Canvas('canvas');
        var parent = this;
        canvas.setBackgroundImage("static/assets/soccer-pitch.png");
        canvas.selection = false; // disable group selection
        //canvas.renderAll()
        canvas.on('mouse:down', function(options) {
            console.log(options.e.clientX, options.e.clientY);
            if (options.target) {
                console.log('Shot clicked ');
                console.log(' - id     : ' + options.target.shot.id);
                console.log(' - player : ' + options.target.shot.player_match.player.name);
                console.log(' - scored : ' + options.target.shot.scored);
                parent.selectedShot = options.target.shot.id;
                parent.selectedShot = JSON.parse(JSON.stringify(options.target.shot));

            }
        });
        this.canvas = canvas


    },
    computed: {
        //console.log("shots.length " + this.shots.length);
        //refreshCanvas()
        selectedShotData: function () {
            return _.find(this.shots, {id: this.selectedShot})
        }

    },
    methods: {
        refreshCanvas: function (event) {
            console.log("REFRESH CANVAS")

        },
        refreshCanvas2: function (event) {
            alert("refreshCanvas2");
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