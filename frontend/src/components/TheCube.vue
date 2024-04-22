<script setup lang="ts">
import { onMounted, reactive, type Ref, ref, watch, getCurrentInstance } from 'vue'
import { getData } from '@/utils/resources'
import LinesChart from '@/components/LinesChart.vue'
import {toColor, calculateHeat, map, stepHeat} from '@/utils/utils'
import { useGlobalStorage } from '@/stores/globalStorage'
import { storeToRefs } from 'pinia'

const storage = useGlobalStorage()
let {currentIndex, current, outside, inside, dataFetched, playBtn, dates, dates_view,
  temperatures, temperatures_view, inside_temperatures, inside_temperatures_view} = storeToRefs(storage)

let rotationX = 0;
let rotationY = 0;
let cubeColor = ref('hsl(90, 100%, 50%)');

const pause = defineModel()

let timer = -1

onMounted(() => {
  getData().then(res => {
    /*console.log('FOO', storage.currentIndex)
    storage.$patch({currentIndex: 17});
    console.log('Bar', storage.currentIndex)*/



    console.log(res.temperatures)
    console.log(storage.temperatures.length)
    storage.$patch({temperatures: res.temperatures});
    console.log('BOB', storage.temperatures.length)
    storage.$patch({temperatures_view: res.temperatures});
    storage.$patch({dates: res.dates});
    storage.$patch({dates_view: res.dates});
    storage.$patch({dataFetched: true});
    storage.$patch({inside_temperatures: [21]});
    storage.$patch({inside_temperatures_view: [21]});

    // storage.$patch({current: dates[0].toLocaleTimeString()});
    // outside.value = temperatures[0];
    // inside.value = INITIAL_HEAT;
  });
  // https://dataset.api.hub.geosphere.at/v1/openapi-docs
  // https://dataset.api.hub.geosphere.at/v1/station/historical/klima-v1-10min?parameters=RR&start=2021-01-01T00%3A00&end=2021-01-01T00%3A00&station_ids=5882&output_format=geojson
})

storage.$subscribe((mutation, state) => {
  /*console.log(mutation)
  console.log(state)
  console.log(mutation.type, mutation.storeId, mutation.payload)*/
})

watch(() => storage.currentIndex, async (newValue, oldValue) => {
  if (newValue >= 145) {
    currentIndex.value = oldValue
    return
  }
  // current.value = dates[newValue].toLocaleTimeString();
  // outside.value = temperatures.value[newValue];
  storage.$patch({outside: temperatures.value[newValue]})

  //let heat = calculateHeat(newValue, inside.value, outside.value);
  let heat = stepHeat(newValue, inside.value, outside.value);
  if (newValue == 0) {
    heat = 21;
  }
  inside.value = heat;
  inside_temperatures.push(heat);
  let color = toColor(heat)
  let cube = document.querySelector<HTMLElement>('.cube')
  if (cube !== null) {
    let children = Array.from(cube.children as HTMLCollectionOf<HTMLElement>)
    for (const child of children) {
      child.style.backgroundColor = `hsl(${color}, 100%, 50%)`;
    }
  }
})
/*
watch(pause, async(newValue, oldValue) => {

})
*/
function play(timeout = 1000) {
  if (timer !== -1) {
    clearInterval(timer)
    timer = -1
    playBtn.value = 'Play'
  } else {
    step()
    timer = setInterval(step, timeout)
    playBtn.value = 'Pause'
  }
}

function fast() {
  play(250)
}

function step() {
  storage.$patch({currentIndex: storage.currentIndex + 1})
  storage.$patch({temperatures_view: storage.temperatures.slice(0, storage.currentIndex)})
  storage.$patch({dates_view: storage.dates.slice(0, storage.currentIndex)})
  storage.$patch({inside_temperatures_view: storage.inside_temperatures.slice(0, storage.currentIndex)})
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
      <v-btn variant="outlined" @click="step()">
        Step
      </v-btn>
      <v-btn variant="outlined" @click="play()">
        {{ playBtn }}
      </v-btn>
      <v-btn variant="outlined" @click="fast()">
        Fast
      </v-btn>
      <v-icon icon="mdi-home" />
      <v-icon>mdi-home</v-icon>
    </div>
    <div class="d-inline">
      {{currentIndex}}
    </div>
     -
    <div class="d-inline">
      {{current}}
    </div>
  </div>
  <div class="controls" v-if="dataFetched">
    <input type="range" min="0" max="144" value="0" v-model="storage.currentIndex" />
  </div>
  <div>
    <LinesChart v-if="dataFetched"
                id="temperature_plot"
                :key="storage.currentIndex"
                :keys="storage.dates"
                :axes="['Outside Temperature', 'Inside Temperature']"
                :values="[storage.temperatures_view, storage.inside_temperatures_view]"/>
    <p v-else>Loading...</p>
  </div>
  <div class="stats">
    <div>
      Outside temperature:
      <div class="font-weight-bold d-inline">{{outside}}</div>°C
    </div>
    <div>
      Inside temperature:
      <div class="font-weight-bold d-inline">{{Math.round(inside * 100) / 100}}</div>°C
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
      <!--<SolarPanel/>-->
    </div>
  </div>
  <!--<Spectator/>-->
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
  --side-length: 250px;
  perspective: 1000px;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 600px;
  border: solid 1px black;
  width: 100%;
}

.cube {
  width: var(--side-length);
  height: var(--side-length);
  position: relative;
  transform-style: preserve-3d;
  transition: transform 0.5s;
  transform: rotateX(-20deg) rotateY(35deg);
  /*transform: rotateX(-25deg) rotateY(45deg);*/
}

.face {
  position: absolute;
  width: var(--side-length);
  height: var(--side-length);
  border: 1px solid #000;
  opacity: 0.8;
  background-color: hsl(0, 100%, 50%);
}

.front {
  transform: rotateY(0deg) translateZ(calc(var(--side-length) / 2));
}

.back {
  transform: rotateY(180deg) translateZ(calc(var(--side-length) / 2));
}

.left {
  transform: rotateY(-90deg) translateZ(calc(var(--side-length) / 2));
}

.right {
  transform: rotateY(90deg) translateZ(calc(var(--side-length) / 2));
}

.top {
  transform: rotateX(90deg) translateZ(calc(var(--side-length) / 2));
}

.bottom {
  transform: rotateX(-90deg) translateZ(calc(var(--side-length) / 2));
}

input[type="range"] {
  width: 100%;
  margin-top: 20px;
}
</style>
