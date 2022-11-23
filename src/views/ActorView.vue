<template>
    <div class="actor-view-container">
        <Timeline :timeline_data="test_data"></Timeline>
    </div>
</template>

<script setup lang="ts">
import Timeline from '../components/Timeline.vue';
import * as vue from "vue"
import { Ref, ref } from "vue"

const server_address = vue.inject("server_address")
const artists: Ref<any[]> = ref([])
const target_artist: Ref<any> = ref(undefined)
const target_artist_career: Ref<any> = ref(undefined)
vue.onMounted(() => {
    get_artists()
    target_artist.value = 'nm0000375'
    get_career(target_artist.value)
})

async function get_career(artist) {
    await fetch(`${server_address}/data/career/${artist}`)
        .then(res => res.json())
        .then(json => {
            target_artist_career.value = json
            console.log("career fetched", json)
        })
}

async function get_artists() {
    await fetch(`${server_address}/data/artists`)
        .then(res => res.json())
        .then(json => {
            artists.value = json
            console.log("artists fetched", json)
        })
}

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