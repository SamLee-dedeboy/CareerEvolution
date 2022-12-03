<template>
    <div class="timeline-container">
        <div class="description-container" v-if='artist_info' >
            <div class="actor-info">
                <h2> {{ artist_info.name }} </h2>
                <br>
                Primary Profession: {{ artist_info.primaryProfession }}
                <br>
                Known Titles: {{ artist_info.knownTitles.join(", ") }}
            </div>
            <div v-for="(section, section_index) in section_descriptions" 
                :id="'section_'+section_index" 
                class="section"
                :style="{top: section_offsets[section_index] + 'px'}"
                >
                <h3 class='section-header'> {{ section.header }} </h3>
                <div class="scrolled-paragraphs">
                    <div v-for="paragraph in section.descriptions" class='section-description'> 
                        <span v-for="(sentence, sentence_index) in paragraph[Object.keys(paragraph)[0]]" class="sentence" :id="`sentence_${Object.keys(paragraph)[0]}_${sentence_index}`">
                            {{ sentence }} &#8202; 
                        </span>
                    </div>
                </div>
            </div>
        </div>
        <svg :class="svgClass"></svg>
        <div class="tooltip" v-if='tooltip_content'>
            Title:
            <span class='tooltip-title'>  {{ tooltip_content.title }} </span>
            <br>
            Year:
            <span class='tooltip-year'>  {{ tooltip_content.year }} </span>
            <br>
            Genres: 
            <!-- <span class='tooltip-genre' v-for="genre in tooltip_content.genre.split(',')"> {{ genre }} </span> -->
            <span class='tooltip-genre'> {{ tooltip_content.genre }} </span>
            <br>
            IMDb Votes:
            <span class='tooltip-votes'> {{ tooltip_content.votes }} </span>
            <br>
            IMDb Rating:
            <span class='tooltip-rating'> {{ tooltip_content.rating }} </span>
        </div>
        <!-- <img src=action.svg class=action> -->
    </div>
</template>
<script setup lang="ts">
import * as d3 from "d3"
import * as vue from "vue"
import { Ref, ref } from "vue"
import { Timeline, TimelineConfig } from "./charts/Timeline"
import scroller from "./scroller"

const props = defineProps({
    artist_info: Object as () => any,
    timeline_data: Object as () => any,
    section_descriptions: Object as () => any[],
})
const svgClass = "timeline-svg"
const svgSelector = vue.computed(() => `.${svgClass}`)
const section_offsets: Ref<number[]> = ref([])
const timeline = new Timeline(svgSelector.value, {
    width: Math.min(700, (window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth)*0.6),
    tracks: {
        "actor": "#F0F0C9",
        "producer": "#72DDF7",
        "director": "#E7C8DD",
        "writer": "#FA824C",
    },
})

vue.watch(() => props.section_descriptions, () => {
    console.log(props.section_descriptions)
})
const tooltip_content: Ref<any> = ref(undefined)
vue.watch(() => props.timeline_data, () => {
    if(props.timeline_data !== undefined) {
        timeline.init(props.timeline_data, tooltip_content)
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
        // highlight vis
        d3.selectAll('.step').each(function (d, i) {
            d3.select(this).selectAll("text").style("opacity", i === index? 1 : 0.05)
        })

        // }).selectAll("text")
        // .style('opacity', function (d, i) { return i === index ? 1 : 0.05; });

        // highlight section description
        const active_step = d3.selectAll(".step").filter((d, i) => i === index)
        const active_stage = d3.select(`#section_${active_step.data()[0].stage}`)
        const active_sentence_infos = active_step.data()[0].snippet.map(snippet => { return {"p": snippet.p, "index": snippet.index} })
        console.log(active_step.data()[0], active_step.data()[0].stage, active_sentence_infos)
        d3.selectAll("span.sentence").style("background", "unset")
        // d3.selectAll("image").style("opacity", 1)
        active_sentence_infos.forEach(sentence_info => {
            active_stage.select(`span#sentence_${sentence_info.p}_${sentence_info.index}`).style("background", "yellow")
        })

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
    height: inherit;
}

.scrolled-paragraphs {
    overflow-y: auto;
    height: 600px;
}

:deep(.active) {
    position: fixed;
    top: 28% !important;
    visibility: visible;
    opacity: 1;
}
.description-container {
  width: 30%;
  display: flex;
  flex-direction: column;
  text-align: center;
  justify-content: center;
  margin-left: 2%;
}

.action {
    filter: invert(21%) sepia(19%) saturate(4450%) hue-rotate(315deg) brightness(93%) contrast(91%);
    /* background-color: red;
    mask: url(action.svg) no-repeat center / contain;
    -webkit-mask: url(action.svg) no-repeat center / contain; */
    position:absolute;
    left: 1%;
    top: 1%;
    width: 50px;
    height: 50px;
}
.section-description {
  text-align: left;
  margin-top: 20px;
}
.tooltip {
    position: absolute;
    z-index: 1000;
    pointer-events: none;
    text-align: left;
    background: white;
    border: solid 3px black;
    padding: 5px;
}
.actor-info {
    position: fixed;
    top: 8%;
    width: inherit;
}
</style>
