<template>
    <div class="actor-graph-container">
        <svg :class="svgClass"></svg>
    </div>
</template>
<script setup lang="ts">
import * as d3 from "d3"
import * as vue from "vue"
import { Ref, ref } from "vue"
import { ActorNetwork } from "./charts/ActorNetwork"

const svgClass = "actor-graph-svg"
const svgSelector = vue.computed(() => `.${svgClass}`)
vue.onMounted(() => {
    const actor_graph = new ActorNetwork(svgSelector.value)
    actor_graph.init()
})

</script>
