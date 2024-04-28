<script setup lang="ts">
import { onMounted, reactive, type Ref, ref, watch, getCurrentInstance } from 'vue'
import { getData, simulate } from '@/utils/resources'
import LinesChart from '@/components/LinesChart.vue'
import {toColor, calculateHeat, map, stepHeat} from '@/utils/utils'
import { Appliance, Battery, Generator } from '@/@types/components'

const INITIAL_HEAT = 21;

let currentIndex = ref(0);
let current_time = ref('');
let current_date = ref('');
let outside = ref(0);
let inside = ref(INITIAL_HEAT);
let dataFetched: Ref<boolean> = ref(false);
let playBtn = ref('Play')

let dates: Date[] = [];
let dates_view: Date[] = [];

let temperatures: number[] = [];
let temperatures_view: Ref<number[]> = ref([]);

let inside_temperatures: number[] = [];
let inside_temperatures_view: Ref<number[]> = ref([]);

let radiations: number[] = [];
let radiations_view: Ref<number[]> = ref([]);

let winds: number[] = [];
let winds_view: Ref<number[]> = ref([]);

let money: number[] = [];
let money_view: Ref<number[]> = ref([]);

let generation: {"SolarPanel": number[], "Windturbine": number[]} = {"SolarPanel": [], "Windturbine": []};
let generation_view: Ref<{"SolarPanel": number[], "Windturbine": number[]}> = ref({"SolarPanel": [], "Windturbine": []});

let battery_level: number[] = [];
let battery_level_view: Ref<number[]> = ref([]);

let rotationX = 0;
let rotationY = 0;
let cubeColor = ref('hsl(90, 100%, 50%)');

const pause = defineModel()

let timer = -1
const lookback = 72

onMounted(() => {
})

watch(currentIndex, async (newValue, oldValue) => {
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

function show_cube_temperature(inner_temperature: number) {
  let color = toColor(inner_temperature)
  let cube = document.querySelector<HTMLElement>('.cube')
  if (cube !== null) {
    let children = Array.from(cube.children as HTMLCollectionOf<HTMLElement>)
    for (const child of children) {
      child.style.backgroundColor = `hsl(${color}, 100%, 50%)`
    }
  }
}

function step() {
  currentIndex.value ++;
  simulate(currentIndex.value, currentIndex.value).then(res => {
    let date_raw = res['environment']['dates'];
    let date = new Date(date_raw);
    current_time.value = date.toLocaleTimeString('de-DE');
    current_date.value = date.toLocaleDateString('de-DE');
    dates.push(date);

    let radiation = res['environment']['radiations'];
    radiations.push(radiation);

    let temperature = res['environment']['temperatures'];
    outside.value = temperature;
    temperatures.push(temperature);

    let wind = res['environment']['winds'];
    let wind_direction = res['environment']['wind_directions'];

    let inner_temperature = res['environment']['inner_temperature'];
    inside.value = inner_temperature;
    inside_temperatures.push(inner_temperature);
    show_cube_temperature(inner_temperature);

    let money = res['environment']['money'];

    for (const appliance_raw of res['appliances']) {
      let appliance = new Appliance(appliance_raw);
    }
    for (const generator_raw of res['generators']) {
      let generator = new Generator(generator_raw);
      if (['SolarPanel', 'Windturbine'].includes(generator.name)) {
        generation[generator.name].push(generator.supply.value);
      }
    }
    let battery = new Battery(res['battery']);
    battery_level.push(battery.level.value);

    if (currentIndex.value > 2) {
      dataFetched.value = true;
      let begin = Math.max(0, currentIndex.value - lookback); // only watch back 12h
      dates_view = dates.slice(begin, currentIndex.value);
      temperatures_view.value = temperatures.slice(begin, currentIndex.value);
      inside_temperatures_view.value = inside_temperatures.slice(begin, currentIndex.value);
      radiations_view.value = radiations.slice(begin, currentIndex.value);
      generation_view.value['SolarPanel'] = generation['SolarPanel'].slice(begin, currentIndex.value);
      generation_view.value['Windturbine'] = generation['Windturbine'].slice(begin, currentIndex.value);
      battery_level_view.value = battery_level.slice(begin, currentIndex.value);
    }
  });
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
      {{ current_time }}
    </div>
    -
    <div class="d-inline">
      {{ current_date }}
    </div>
  </div>
  <div class="controls" v-if="dataFetched">
    <input type="range" min="0" max="{{lookback}}" value="0" v-model="currentIndex" />
  </div>
  <div>
    <LinesChart v-if="dataFetched"
                id="temperature_plot"
                :key="currentIndex"
                :keys="dates_view"
                :axes="['Outside Temperature', 'Inside Temperature']"
                :values="[temperatures_view, inside_temperatures_view]"/>

    <LinesChart v-if="dataFetched"
                id="radiation_plot"
                :key="currentIndex"
                :keys="dates_view"
                :axes="['Radiation']"
                :values="[radiations_view]"/>

    <LinesChart v-if="dataFetched"
                id="solar_plot"
                :key="currentIndex"
                :keys="dates_view"
                :axes="['Solar generation', 'Windturbine generation']"
                :values="[generation_view['SolarPanel'], generation_view['Windturbine']]"/>

    <LinesChart v-if="dataFetched"
                id="battery_plot"
                :key="currentIndex"
                :keys="dates_view"
                :axes="['Battery Level']"
                :values="[battery_level_view]"/>
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
