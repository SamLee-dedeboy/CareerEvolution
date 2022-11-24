<template>
    <div class="actor-view-container">
        <Timeline :timeline_data="test_data"></Timeline>
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

</script>