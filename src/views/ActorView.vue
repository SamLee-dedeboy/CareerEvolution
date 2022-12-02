<template>
    <div class="actor-view-container">
        <Timeline :timeline_data="target_artist_career" :section_descriptions="stage_descriptions"></Timeline>
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
const stage_descriptions: Ref<any> = ref(undefined)
vue.onMounted(() => {
    // target_artist.value = 'nm0000375'
    target_artist.value = 'nm0413168'
    // target_artist.value = 'nm0005351'
    // target_artist.value = 'nm0426059'
    get_career(target_artist.value)
})

async function get_career(artist) {
    await fetch(`${server_address}/data/career/${artist}`)
        .then(res => res.json())
        .then(json => {
            target_artist_career.value = json
            stage_descriptions.value = json.map(stage => {
                return {
                    "header": stage.header,
                    "descriptions": stage.paragraphs
                    // "descriptions": stage.paragraphs.map(paragraph => paragraph[Object.keys(paragraph)[0]])
                }
            })
            console.log(stage_descriptions.value)
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

</script>