<template>
    <div class="actor-view-container">
        <Timeline :timeline_data="test_data" :section_desciptions="test_descriptions"></Timeline>
    </div>
</template>

<script setup lang="ts">
import Timeline from '../components/Timeline.vue';

const test_data = [
    { // section
        header: "stage 1",
        movies: [0, 0, 0, 0],
    },
    { // section
        header: "stage 2",
        movies: [1, 1, 1, 1],
    },
    { // section
        header: "stage 3",
        movies: [2, 2, 2, 2],
    },
    { // section
        header: "stage 3",
        movies: [3, 3, 3, 3],
    },
]

const test_descriptions = [
    {
        header: "Early Stage",
        description: "At his early stage of career, he was someweqewqewqewqewqewqewqewqewq"
    },
    {
        header: "Middle Stage",
        description: "At his middle stage of career, he was someweqewqewqewqewqewqewqewqewq"
    },
    {
        header: "Late Stage",
        description: "At his late stage of career, he was someweqewqewqewqewqewqewqewqewq"
    },
]

</script>