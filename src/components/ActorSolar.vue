<template>
    <div class="actor-solar-container">
        <svg :class="svgClass"></svg>
    </div>
</template>
<script setup lang="ts">
import * as d3 from "d3"
import * as vue from "vue"
import { Ref, ref } from "vue"
import { ActorSolar } from "./charts/ActorSolar";

const svgClass = "actor-solar-svg"
const svgSelector = vue.computed(() => `.${svgClass}`)
vue.onMounted(() => {
    const actor_solar = new ActorSolar(svgSelector.value)
    actor_solar.init()
})

</script>
