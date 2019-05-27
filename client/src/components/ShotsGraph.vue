<template>
  <div>
  <v-layout justify-center row>
    <svg id="shots-chart" :width="width" :height="height"
      v-on:click="clickCanvas"
    >

      <!-- field lines -->
      <g  v-for="field_rect in fieldLinesRects"
                 :value="field_rect" :key="field_rect.id">

        <rect class="field-line-rect"
              :x="field_rect.x"
              :y="field_rect.y"
              :height="field_rect.height"
              :width="field_rect.width">
        </rect>
      </g>

      <!-- field text -->
      <g v-for="field_text in fieldLabels"
         :value="field_text" :key="field_text.id">

        <text class="field-text" text-anchor="middle"
              :x="field_text.x"
              :y="field_text.y"
        >
          {{field_text.label}}
        </text>
      </g>

      <!-- shots -->
      <g v-for="shot in shots"
         :value="shot" :key="shot.id">

        <!-- shot circle -->
        <circle class="shot-circle"
          :cx="shot.x"
          :cy="shot.y"
          :r="10"
          :stroke="shotStrokeColor(shot.by_opponent)"
          :fill="shotFillColor(shot.id, shot.scored, shot.on_target)"
          v-on:mouseover="shotMouseOverEvent(shot)"
          v-on:click="onClickShot(shot)"
        >
        </circle>

        <!-- shot text -->
        <text class="shot-text"
          :x="shot.x"
          :y="shot.y + 5"
        >
        {{ shot.by_opponent ? "-" : shot.player_number  }}
        </text>
      </g>

    </svg>
  </v-layout>
  <v-layout justify-center row>

      Grey: off target, Green: on target, Red: scored
  </v-layout>
  </div>
</template>
<script>

export default {
  props: ['shots', 'activeShotId', 'onClickShot', 'onClickCanvas', 'showHiddenArea'],
  data () {
    return {
      height: 700,
      fieldLinesRects: [
        // rectangles in top half
        { id: 0, x: 10, y: 20, width: 430, height: 330 },
        { id: 1, x: 100, y: 20, width: 245, height: 100 },
        { id: 2, x: 170, y: 20, width: 115, height: 30 },
        { id: 3, x: 200, y: 18, width: 55, height: 4 },
        // bottom half
        { id: 4, x: 10, y: 350, width: 430, height: 330 },
        { id: 5, x: 100, y: 580, width: 245, height: 100 },
        { id: 6, x: 170, y: 650, width: 115, height: 30 },
        { id: 7, x: 200, y: 678, width: 55, height: 4 },
        // hidden
        { id: 8, x: 460, y: 20, width: 70, height: 660 }
      ],
      fieldLabels: [
        { id: 10, x: 225, y: 250, label: "Team's attempts"},
        { id: 11, x: 225, y: 450, label: "Opponent's attempts"}
      ]
    }
  },
  methods: {
    shotMouseOverEvent (shot) {

    },
    shotClickEvent (shot) {
      console.log(shot)
    },
    shotStrokeColor (by_opponent) {
      if (by_opponent) {
        return 'white'
      }
      return 'black'
    },
    shotFillColor (id, scored, on_target) {
      if (id === this.activeShotId) {
        return 'yellow'
      }
      if (scored) {
        return 'red'
      }
      return on_target ? 'PaleGreen' : 'grey'
    },
    clickCanvas (e) {
      if (typeof this.onClickCanvas !== 'undefined') {
        this.onClickCanvas(e.offsetX, e.offsetY)
      }
    }
  },
  computed: {
    width: function () {
      if (this.showHiddenArea) {
        return 550
      }
      return 450
    }
  }
}
</script>

<style>
#shots-chart {
  background-color: DarkGreen;
  border: 1px solid black;
}
.field-line-rect {
  stroke: green;
  stroke-width: 3;
  fill: transparent;

}
.field-text {
  font-size: 30px;
  opacity: 0.5;
}
.shot-circle {
  opacity: 0.75;
}
.shot-text {
  pointer-events: none;
  font-weight: bold;
  text-anchor: middle;
}
</style>
