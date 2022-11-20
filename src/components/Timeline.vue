<template>
    <div class="timeline-container">
        <svg :class="svgClass"></svg>
    </div>
</template>
<script setup lang="ts">
import * as d3 from "d3"
import * as vue from "vue"
import { Ref, ref } from "vue"
import { Timeline, TimelineConfig } from "./charts/Timeline"
import scroller from "./scroller"

const props = defineProps({
    timeline_data: Object as () => any,
})
const svgClass = "timeline-svg"
const svgSelector = vue.computed(() => `.${svgClass}`)
const timeline = new Timeline(svgSelector.value, {
    width: Math.min(1100, window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth),
    tracks: {
        "actor": "#872B3D",
        "director": "#56D3CD",
        "writer": "#FC6940",
        "producer": "#D7D160",
    },
})

vue.onMounted(() => {
    timeline.init(props.timeline_data)
    // setupScroller()
})


function setupScroller() {
    // setup scroll functionality
    let scroll:any = scroller.scroller()
        .container(d3.select('#graphic'));

    // pass in .step selection as the steps
    scroll(d3.selectAll('.step'));

    // setup event handling
    scroll.on('active', function (index) {
        // highlight current step text
        d3.selectAll('.step')
        .style('opacity', function (d, i) { return i === index ? 1 : 0.1; });

        // activate current section
        timeline.activate(index);
    });

    scroll.on('progress', function (index, progress) {
        timeline.update(index, progress);
    });

}

</script>
