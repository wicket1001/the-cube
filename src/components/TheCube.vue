<script setup lang="ts">
import { onMounted, reactive, type Ref, ref, watch, getCurrentInstance } from 'vue'
import { getData } from '@/utils/resources'
import LinesChart from '@/components/LinesChart.vue'
import {toColor, calculateHeat, map, stepHeat} from '@/utils/utils'
import { useGlobalStorage } from '@/stores/globalStorage'

const storage = useGlobalStorage()

const INITIAL_HEAT = 21;

let currentIndex = ref(0);
let current = ref('');
let outside = ref(0);
let inside = ref(INITIAL_HEAT);
let dataFetched: Ref<boolean> = ref(false);
let playBtn = ref('Play')

let dates: Date[] = [];
let dates_view: Ref<Date[]> = ref([]);

let temperatures: number[] = [];
let temperatures_view: Ref<number[]> = ref([]);

let inside_temperatures: number[] = [];
let inside_temperatures_view: Ref<number[]> = ref([]);

let rotationX = 0;
let rotationY = 0;
let cubeColor = ref('hsl(90, 100%, 50%)');

const pause = defineModel()

let timer = -1

onMounted(() => {
  getData().then(res => {
    temperatures = res.temperatures;
    temperatures_view.value = res.temperatures;
    dates = res.dates;
    dates_view.value = res.dates;
    dataFetched.value = true;
    inside_temperatures = [21];
    inside_temperatures_view.value = [21];

    current.value = dates[0].toLocaleTimeString();
    outside.value = temperatures[0];
    inside.value = 21;
  });
  // https://dataset.api.hub.geosphere.at/v1/openapi-docs
  // https://dataset.api.hub.geosphere.at/v1/station/historical/klima-v1-10min?parameters=RR&start=2021-01-01T00%3A00&end=2021-01-01T00%3A00&station_ids=5882&output_format=geojson
})

watch(currentIndex, async (newValue, oldValue) => {
  if (newValue >= 145) {
    currentIndex.value = oldValue
    return
  }
  current.value = dates[newValue].toLocaleTimeString();
  outside.value = temperatures[newValue];

  //let heat = calculateHeat(newValue, inside.value, outside.value);
  let heat = stepHeat(newValue, inside.value, outside.value);
  if (newValue == 0) {
    heat = INITIAL_HEAT;
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

watch(pause, async(newValue, oldValue) => {

})

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
  currentIndex.value ++
  // document.getElementById("temperature_plot").$forceUpdate();
  //const instance = getCurrentInstance();
  //instance.proxy.$forceUpdate();
  //console.log(temperatures.length)
  temperatures_view.value = temperatures.slice(0, currentIndex.value)
  //console.log(temperatures_view.value.length)
  //dates.push(dates[dates.length - 1])
  //dates.pop()
  dates_view.value = dates.slice(0, currentIndex.value)
  inside_temperatures_view.value = inside_temperatures.slice(0, currentIndex.value)
  //console.log(inside_temperatures)

  //console.log(dates_view.value)
  //console.log('BOB')
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
    <input type="range" min="0" max="144" value="0" v-model="currentIndex" />
  </div>
  <div>
    <LinesChart v-if="dataFetched"
                id="temperature_plot"
                :key="currentIndex"
                :keys="dates"
                :axes="['Outside Temperature', 'Inside Temperature']"
                :values="[temperatures_view, inside_temperatures_view]"/>
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
