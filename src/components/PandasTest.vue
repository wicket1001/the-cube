<script setup lang="ts">
import {ref, onMounted} from 'vue'
import axios from 'axios'
import type { Geosphere } from '@/@types/geosphere'

const greeting = ref('Hello World!')
const host = 'https://dataset.api.hub.geosphere.at'
const version = 'v1'

let apiData: [number] = []

onMounted(() => {
  console.log('PAIN')
  let type = 'station' // ?station_ids=1,2,3
  let mode = 'historical'
  let resource_id = 'klima-v1-10min'

  let url = `${host}/${version}/${type}/${mode}/${resource_id}` // /metadata

  // https://dataset.api.hub.geosphere.at/v1/station/historical/klima-v1-10min?parameters=RR&start=2021-01-01T00%3A00&end=2021-01-01T00%3A00&station_ids=5882&output_format=geojson
  axios.get(url, {
    params: {
      parameters: "RR",
      station_ids: 5882,
      start: "2021-01-20T00:00",
      end: "2021-01-21T00:00",
      output_format: 'geojson'
    }
  })
    .then((response) => {
      let data: Geosphere = response.data
      console.log(data)
      apiData = data['features'][0]['properties']['parameters']['RR']['data']
      console.log(apiData)
    })
    .catch((error) => {
      console.error('Error fetching data:', error)
    })
})
</script>

<template>
  <div>
    <h1>Data</h1>
    <ul v-if="!!apiData.length">
      <li v-for="item in apiData" :key="item.id">
        {{item}}
      </li>
    </ul>
    <p v-else>Loading....</p>
  </div>
</template>

<style scoped>

.greetings h1,
.greetings h3 {
  text-align: center;
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
}
</style>
