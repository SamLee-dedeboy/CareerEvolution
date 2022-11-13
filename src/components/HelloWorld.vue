<script setup lang="ts">
import { ref } from 'vue'
import * as vue from "vue"
const server_address = vue.inject("server_address")

vue.onMounted(() => {
  test_fetch()
})

async function test_fetch() {
  await fetch(`${server_address}/data/artists`)
    .then(res => res.json())
    .then(json => {
        console.log(json)
    })
}
// async function test_post() {
//   await fetch(`${server_address}/processed_data/ids_to_articles`, {
//       method: "POST",
//       headers: {
//           "Accept": "application/json",
//           "Content-Type": "application/json"
//       },
//       body: JSON.stringify(article_ids)
//   })
//       .then(res => res.json())
//       .then(json => {
//           target_articles.value = json
//           console.log("articles fetched")
//       }) 
// }

defineProps<{ msg: string }>()

const count = ref(0)
</script>

<template>
  <h1>{{ msg }}</h1>

  <div class="card">
    <button type="button" @click="count++">count is {{ count }}</button>
    <p>
      Edit
      <code>components/HelloWorld.vue</code> to test HMR
    </p>
  </div>

  <p>
    Check out
    <a href="https://vuejs.org/guide/quick-start.html#local" target="_blank"
      >create-vue</a
    >, the official Vue + Vite starter
  </p>
  <p>
    Install
    <a href="https://github.com/johnsoncodehk/volar" target="_blank">Volar</a>
    in your IDE for a better DX
  </p>
  <p class="read-the-docs">Click on the Vite and Vue logos to learn more</p>
</template>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
