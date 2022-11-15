<template>
    <div class="timeline-container">
        <svg :class="svgClass"></svg>
    </div>
</template>
<script setup lang="ts">
import * as d3 from "d3"
import * as vue from "vue"
import { Ref, ref } from "vue"
import { Timeline } from "./charts/Timeline"

const svgClass = "timeline-svg"
const svgSelector = vue.computed(() => `.${svgClass}`)
vue.onMounted(() => {
    const timeline = new Timeline(svgSelector.value)
    timeline.init()
})

</script>
