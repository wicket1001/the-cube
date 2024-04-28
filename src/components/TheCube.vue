<script setup lang="ts">
import { onMounted, reactive, type Ref, ref, watch, getCurrentInstance } from 'vue'
import { getData, simulate } from '@/utils/resources'
import LinesChart from '@/components/LinesChart.vue'
import {toColor, calculateHeat, map, stepHeat} from '@/utils/utils'
import { Appliance, Battery, Generator } from '@/@types/components'

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

function step() {
  currentIndex.value ++;
  simulate(currentIndex.value, currentIndex.value).then(res => {
    let date_raw = res['environment']['dates'];
    let date = new Date(date_raw);
    current.value = date.toLocaleTimeString();
    dates.push(date);

    let radiation = res['environment']['radiations'];

    let temperature = res['environment']['temperatures'];
    outside.value = temperature;
    temperatures.push(temperature);

    let wind = res['environment']['winds'];
    let wind_direction = res['environment']['wind_directions'];

    let inner_temperature = res['environment']['inner_temperature'];
    inside.value = inner_temperature;
    inside_temperatures.push(inner_temperature);

    let money = res['environment']['money'];

    for (const appliance_raw of res['appliances']) {
      let appliance = new Appliance(appliance_raw);
    }
    for (const generator_raw of res['generators']) {
      let generator = new Generator(generator_raw);
    }
    let battery = new Battery(res['battery']);

    if (currentIndex.value > 2) {
      dataFetched.value = true;
      temperatures_view.value = temperatures.slice(0, currentIndex.value);
      inside_temperatures_view.value = inside_temperatures.slice(0, currentIndex.value);
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
