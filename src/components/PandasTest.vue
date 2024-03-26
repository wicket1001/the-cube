<script setup lang="ts">
import {ref, onMounted} from 'vue'
import axios from 'axios'
import type { Dates, Geosphere, GeosphereRaw } from '@/@types/geosphere'

const greeting = ref('Hello World!')
const host = 'https://dataset.api.hub.geosphere.at'
const version = 'v1'

let apiData: [number] = []

const start = "2021-01-20T00:00"
const end = "2021-01-21T00:00"
const parameter = "tl"

let currentIndex = 0
let current = new Date()
let dates: [Date] = []

onMounted(() => {
  const type = 'station' // ?station_ids=1,2,3
  const mode = 'historical'
  const resource_id = 'klima-v2-10min'

  let url = `${host}/${version}/${type}/${mode}/${resource_id}` // /metadata

  // https://dataset.api.hub.geosphere.at/v1/station/historical/klima-v1-10min?parameters=RR&start=2021-01-01T00%3A00&end=2021-01-01T00%3A00&station_ids=5882&output_format=geojson
  axios.get(url, {
    params: {
      parameters: parameter,
      station_ids: 5925, // Wien Innere Stadt
      start: start,
      end: end,
      output_format: 'geojson'
    },
    /*transformResponse: function(data: GeosphereRaw) {
      for (let i = 0; i < data['timestamps'].length; i++) {
        data['timestamps'][i] = new Date(data['timestamps'][i])
      }
      return data
    }*/
  })
    .then((response) => {
      let data: GeosphereRaw = response.data
      apiData = data['features'][0]['properties']['parameters']['tl']['data']
      dates = export_dates(data)['timestamps']
      console.log(apiData)
      console.log(dates)
    })
    .catch((error) => {
      console.error('Error fetching data:', error)
    })
})

function export_dates(data: GeosphereRaw): Dates {
  return { 'timestamps':
      data['timestamps'].map<Date>(item => {
        return new Date(item)
      }
    )
  }
}
</script>

<template>
  <div>
    <h1>Data</h1>
    <p>{{start}}</p>
    <p>{{end}}</p>
    <p>{{current}}</p>
  </div>
  <div class="controls">
    <input type="range" min="0" max="144" value="0" v-model="currentIndex" />
  </div>
  <div>
    <ul v-if="!!apiData.length">
      <li v-for="item in apiData" :key="item">
        {{item}}
      </li>
    </ul>
    <p v-else>Loading....</p>

    <ul v-if="!!dates.length">
      <li v-for="item in dates" :key="item.toLocaleTimeString()" :value="item.toLocaleTimeString()">
        {{item.toLocaleTimeString()}}
      </li>
    </ul>
    <p v-else>Loading...</p>
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

input[type="range"] {
  width: 100%;
  margin-top: 20px;
}
</style>
