<template>
    <div class="actor-view-container">
        <Timeline :timeline_data="test_data"></Timeline>
    </div>
</template>

<script setup lang="ts">
import Timeline from '../components/Timeline.vue';

const test_data = [
    0, 0, 0, 0, 
    1, 1, 1, 1,
    2, 2, 2, 2,
    3, 3, 3, 3,
]

</script>