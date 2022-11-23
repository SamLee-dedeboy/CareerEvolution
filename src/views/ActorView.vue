<template>
    <div class="actor-view-container">
        <Timeline :timeline_data="target_artist_career_data" :section_desciptions="test_descriptions"></Timeline>
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
const target_artist_career_data: Ref<any> = ref(undefined)
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
            target_artist_career_data.value = preprocess_career(target_artist_career.value)
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

// TODO: this should be done in back end 
function preprocess_career(career) {
    // sort movies by year
    career.sort((m1, m2) => +m1.year - +m2.year)
    console.log(career)
    let test_generated_data: any[] = []
    let cur_stage_movies: any[] = []
    let stage_count = 1
    career.forEach(movie => {
        cur_stage_movies.push(movie)
        if(movie.snippet.length != 0) {
            test_generated_data.push({
                header: `stage ${stage_count}`,
                movies: JSON.parse(JSON.stringify(cur_stage_movies))
            })
            cur_stage_movies = []
            stage_count += 1
            // TODO: add stage description
        }
    });
    console.log(test_generated_data)
    return test_generated_data
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