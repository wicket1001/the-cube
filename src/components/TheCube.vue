<script setup lang="ts">
import { onMounted, reactive, type Ref, ref, watch, onBeforeUnmounted } from 'vue'
import { getData } from '@/utils/resources'
import LineChart from '@/components/LineChart.vue'
import {toColor, calculateHeat, map} from '@/utils/utils'

let currentIndex = ref(0);
let current = ref('');
let outside = ref(0);
let inside = ref(21);
let dates: Date[] = [];
let dataFetched: Ref<boolean> = ref(false);

let temperatures: number[];

let rotationX = 0;
let rotationY = 0;
let cubeColor = ref('hsl(90, 100%, 50%)');

let pause = ref('Pause');

onMounted(() => {
  getData().then(res => {
    temperatures = res.temps;
    dates = res.dates;
    dataFetched.value = true;

    current.value = dates[0].toLocaleTimeString();
    outside.value = temperatures[0];
    inside.value = 21;
  });
  // https://dataset.api.hub.geosphere.at/v1/station/historical/klima-v1-10min?parameters=RR&start=2021-01-01T00%3A00&end=2021-01-01T00%3A00&station_ids=5882&output_format=geojson
})

watch(currentIndex, async (newValue, oldValue) => {
  current.value = dates[newValue].toLocaleTimeString();
  outside.value = temperatures[newValue];

  let heat = calculateHeat(newValue, inside.value, outside.value);
  inside.value = heat;
  let color = toColor(heat)
  let children = document.querySelector(".cube").children
  for (const child of children) {
    child.style.backgroundColor = `hsl(${color}, 100%, 50%)`;
  }
})

watch(pause, async(newValue, oldValue) => {
  
})

function play() {
  console.log('BOB', pause.value)
  if (pause.value === 'Pause') {
    pause.value = 'Play'
  }
  if (pause.value === 'Play') {
    pause.value = 'Pause'
  }
}

</script>

<template>
  <div>
    <h1>Data</h1>
    <!--<p>{{start}}</p>
    <p>{{end}}</p>-->
    <!--<datepicker placeholder="Start Date" v-model="start" name="start-date"></datepicker>
    <datepicker placeholder="End Date" v-model="end" name="end-date"></datepicker>-->
    <div>
      <v-btn variant="outlined" @click="currentIndex++">
        Step
      </v-btn>
      <v-btn variant="outlined" @click="play()">
        {{pause}}
      </v-btn>
    </div>
    <p>{{current}}</p>
  </div>
  <div class="controls" v-if="dataFetched">
    <input type="range" min="0" max="144" value="0" v-model="currentIndex" />
  </div>
  <p>
    {{currentIndex}}
  </p>
  <div>
    <LineChart v-if="dataFetched" :keys="dates" :values="temperatures"/>
    <p v-else>Loading...</p>
  </div>
  <div class="stats">
    <div>
      Outside temperature:
      <div>{{outside}}</div>°C
    </div>
    <div>
      Inside temperature:
      <div>{{Math.round(inside * 100) / 100}}</div>°C
    </div>
  </div>
  <div class="cube-container">
    <div class="cube">
      <div class="face front">Front</div>
      <div class="face back">Back</div>
      <div class="face left">Left</div>
      <div class="face right">Right</div>
      <div class="face top">Top</div>
      <div class="face bottom">Bottom</div>
    </div>
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

.cube-container {
  perspective: 1000px;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 50vh;
}

.cube {
  width: 100px;
  height: 100px;
  position: relative;
  transform-style: preserve-3d;
  transition: transform 0.5s;
  transform: rotateX(-25deg) rotateY(45deg);
}

.face {
  position: absolute;
  width: 100px;
  height: 100px;
  border: 1px solid #000;
  opacity: 0.8;
  background-color: hsl(0, 100%, 50%);
}

.front {
  transform: rotateY(0deg) translateZ(50px);
}

.back {
  transform: rotateY(180deg) translateZ(50px);
}

.left {
  transform: rotateY(-90deg) translateZ(50px);
}

.right {
  transform: rotateY(90deg) translateZ(50px);
}

.top {
  transform: rotateX(90deg) translateZ(50px);
}

.bottom {
  transform: rotateX(-90deg) translateZ(50px);
}

input[type="range"] {
  width: 100%;
  margin-top: 20px;
}
</style>
