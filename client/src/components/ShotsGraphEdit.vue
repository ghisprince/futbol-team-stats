<template>
  <div>
    <svg id="shots-chart2"></svg>
    <p>Grey: off target, Green: on target, Red: scored.</p>
  {{ shots }}

  </div>
</template>

<script>
import * as d3 from 'd3';

export default {
  props: ['shots'],
  data () {
    return {
      _svg: "",
      width: 550,
      height: 700
    }
  },
  mounted: function() {
    this.$nextTick(this.load())
  },
  methods: {
    updateYo(x, y) {
      console.log("updateYo " + x + " " + y)
      this.shots[0].x = x
      this.shots[0].y = y
      this.load()
    },
    
    load () {
      const parent = this
      let fieldLinesRects = [
        // rectangles in top half
        { x: 10, y:20, width: 430, height: 330 },
        { x: 100, y:20, width: 245, height: 100 },
        { x: 170, y:20, width: 115, height: 30 },

        // bottom half
        { x: 10, y:350, width: 430, height: 330 },
        { x: 100, y:580, width: 245, height: 100 },
        { x: 170, y:650, width: 115, height: 30 },

        // hidden
        { x: 460, y:20, width: 70, height: 660 }
        ]

      let fieldLabels = [
        { x: 225, y: 250, label: "Team's attempts"},
        { x: 225, y: 450, label: "Opponent's attempts"},
      ]

      let shotFillColor = { off_target: "grey",
                            on_target: "PaleGreen",
                            scored: "red" }

      let shotStrokeColor = { by_opponent: "white", 
                              by_team: "black"}

      let svg  = d3.select('#shots-chart2')
        .attr("width", this.width)
        .attr("height", this.height)
        .style("background-color", "DarkGreen")
        .style('border', '1px solid black')

      svg.selectAll("g").remove()


      let svgRect = svg.append("g")
        .attr("id", "field-rect")
        .selectAll('rect')
        .data(fieldLinesRects)
        .enter()
        .append('rect')
        .attr("x", function (d) { return d.x } )
        .attr("y", function (d) { return d.y })
        .attr("width", function (d) { return d.width })
        .attr("height", function (d) { return d.height })
        .attr('stroke', 'green')
        .attr('stroke-width', 3)
        .attr("fill", "transparent")

      svg.append("g")
        .attr("id", "field-text")
        .selectAll("text")
        .data(fieldLabels)
        .enter()
        .append("text")
        .attr("x", function(d) { return d.x })
        .attr("y", function(d) { return d.y })
        .attr("text-anchor", "middle")
        .style("font-size","30px")
        .style("opacity", 0.5)
        .text(function(d) { return d.label })


      let svgPoints = svg.append("g")
        .attr("id", "shots-point")
        .selectAll("circle")
        .data(this.shots)
        .enter()
        .append("circle")

      let svgPointAtts = svgPoints
        .attr("class", "dot")
        .style("opacity", 1)
        .style("stroke", function (pt) { 
          return shotStrokeColor[pt.by_opponent ? 'by_opponent' : 'by_team']
        })
        .attr("fill", function(pt) {
          if (pt.scored) {
            return shotFillColor['scored']
          }
          return (shotFillColor[pt.on_target ? 'on_target' : 'off_target' ] )
        })
        .attr("cx", function(pt) { return pt.x })
        .attr("cy", function(pt) { return pt.y })
        .attr("r", 10)

      // onclick
      svg.on("click",function () {
        let coords = d3.mouse(this)
        parent.updateYo(coords[0], coords[1])
        console.log(coords)
      })

    },
    handleMouseOver (d, i) {
      console.log("#######2#")
      console.log(d)
      d3.select('circle')
        .attr({"fill": "orange"})
        .attr("r", 7)
    }
  },
  watch: {
    shots: function dataChanged(n, o) {
      console.log("changed")
      this.load()
    }
  },
  computed: {
  }
}
</script>