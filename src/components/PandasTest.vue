<script setup lang="ts">
import { onMounted, reactive, type Ref, ref } from 'vue'
import { getData } from '@/utils/resources'
import LineChart from '@/components/LineChart.vue'

let currentIndex = 0;
let current = new Date();
let dates: Date[] = [];
let dataFetched: Ref<boolean> = ref(false);

let temperatures: number[];

onMounted(() => {
  getData().then(res => {
    temperatures = res.temps;
    dates = res.dates;
    dataFetched.value = true;
  });
  // https://dataset.api.hub.geosphere.at/v1/station/historical/klima-v1-10min?parameters=RR&start=2021-01-01T00%3A00&end=2021-01-01T00%3A00&station_ids=5882&output_format=geojson
})

</script>

<template>
  <div>
    <h1>Data</h1>
    <!--<p>{{start}}</p>
    <p>{{end}}</p>-->
    <!--<datepicker placeholder="Start Date" v-model="start" name="start-date"></datepicker>
    <datepicker placeholder="End Date" v-model="end" name="end-date"></datepicker>-->
    <p>{{current}}</p>
  </div>
  <div class="controls">
    <input type="range" min="0" max="144" value="0" v-model="currentIndex" />
  </div>
  <div>
    <LineChart v-if="dataFetched" :keys="dates" :values="temperatures"/>
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
