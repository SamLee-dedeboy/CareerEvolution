<template>
    <div class="homeview-container">
        <p> Home view</p>
        <ActorNetwork></ActorNetwork>
    </div>
</template>
<script setup lang="ts">
import ActorNetwork from '../components/ActorNetwork.vue';
import { useStore } from 'vuex'
import * as vue from "vue"
const store = useStore()

// test store
const test_store = vue.computed(() => store.state.test)
console.log(test_store.value)

// test backend request
const server_address = vue.inject("server_address")
await fetch(`${server_address}/data/artists`, 
    // {
    //     method: "POST",
    //     headers: {
    //         "Accept": "application/json",
    //         "Content-Type": "application/json"
    //     },
    // }
    )
    .then(res => res.json())
    .then(json => {
        console.log(json)
    })


</script>