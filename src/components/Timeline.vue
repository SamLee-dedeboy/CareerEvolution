<template>
    <div class="timeline-container">
        <div class="description-container">
            <div v-for="(section, index) in section_desciptions" 
                :id="'section_'+index" 
                class="section"
                :style="{top: section_offsets[index] + 'px'}"
                >
                <h4 class='section-header'> {{ section.header }} </h4>
                <div class='section-description'> {{ section.description }} </div>
            </div>

        </div>
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
    section_desciptions: Object as () => any[],
})
const svgClass = "timeline-svg"
const svgSelector = vue.computed(() => `.${svgClass}`)
const section_offsets: Ref<number[]> = ref([])
const timeline = new Timeline(svgSelector.value, {
    width: Math.min(1100, (window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth)*0.6),
    tracks: {
        "actor": "#872B3D",
        "producer": "#D7D160",
        "director": "#56D3CD",
        "writer": "#FC6940",
    },
})
vue.watch(() => props.timeline_data, () => {
    if(props.timeline_data !== undefined) {
        timeline.init(props.timeline_data)
        section_offsets.value = timeline.getSectionOffset()
        setupScroller()

    }
})



function setupScroller() {
    // setup scroll functionality
    let scroll:any = scroller.scroller()
        .container(d3.select('.sections-container'));

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

<style scoped>
.timeline-container {
    display: flex;
}
.section {
    visibility: hidden;
    position: absolute;
    width: inherit;
    opacity: 0;
    transition: visibility 0s, opacity 0.5s linear;

}
:deep(.active) {
    position: fixed;
    top: 15% !important;
    visibility: visible;
    opacity: 1;
}
.description-container {
  width: 30%;
  display: flex;
  flex-direction: column;
  text-align: center;
  justify-content: center;
}
</style>
