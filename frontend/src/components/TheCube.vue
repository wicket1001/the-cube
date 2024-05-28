<script setup lang="ts">
import { onMounted, reactive, type Ref, ref, watch, getCurrentInstance, computed } from 'vue'
import { getData, patch_future, patching, reset_simulation, simulate } from '@/utils/resources'
import Mode from '@/components/LinesChart.vue'
import LinesChart from '@/components/LinesChart.vue'
import WindComponent from '@/components/WindComponent.vue'
import {toColor, calculateHeat, mapping, stepHeat} from '@/utils/utils'
import {
  type IGenerator,
  type Generators,
  type IAppliances,
  type IGrid,
  type Algorithms, bob
} from '@/@types/components'
import { Appliance, Battery, Generator, Grid } from '@/@types/components'
import { Energy, Money, Temperature } from '@/@types/physics'
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import { getMonth, addMonths, addMinutes, differenceInMinutes } from 'date-fns'
import { type ISimulation, Simulation } from '@/@types/simulation'


const INITIAL_HEAT = 21;

// https://dev.to/razi91/vues-new-definemodel-3nd5
let future = defineModel<Date>('future', {default: new Date()});
const presetDates = ref([
  {label: 'Begin', value: new Date(2021, 0, 1, 0, 0, 0)},
  {label: 'End of first year', value: new Date(2022, 0, 1, 0, 0, 0)},
  {label: 'End of simulation', value: new Date(2023, 11, 31, 23, 50, 0)},
  {label: 'Scenario 1', value: new Date(2022, 2, 1, 0, 0, 0)},
  {label: 'Scenario 2', value: new Date(2022, 5, 1, 0, 0, 0)},
  {label: 'Scenario 3', value: new Date(2022, 8, 1, 0, 0, 0)},
  {label: 'Scenario 4', value: new Date(2022, 11, 1, 0, 0, 0)},
]);

let currentIndex = ref(0);
let current_time = ref('');
let current_date = ref('');
let outside = ref(new Temperature(0));
let inside = ref(new Temperature(0));
let dataFetched: Ref<boolean> = ref(false);
let playBtn = ref('Play')

let dates: Date[] = [];
let dates_view: Date[] = [];

let temperatures_graph: {"Outside": Temperature[], "Benchmark First Inside": Temperature[], "Decision First Inside": Temperature[]} =
  {'Outside': [], 'Benchmark First Inside': [], 'Decision First Inside': []};
let temperatures_graph_view: Ref<{"Outside": Temperature[], "Benchmark First Inside": Temperature[], "Decision First Inside": Temperature[]}> =
  ref({'Outside': [], 'Benchmark First Inside': [], 'Decision First Inside': []});

let temperatures: Temperature[] = [];
let temperatures_view: Ref<Temperature[]> = ref([]);

let benchmark_inside_temperatures: Temperature[] = [];
let benchmark_inside_temperatures_view: Ref<Temperature[]> = ref([]);
let decision_inside_temperatures: Temperature[] = [];
let decision_inside_temperatures_view: Ref<Temperature[]> = ref([]);

let precipitations: number[] = [];
let precipitations_view: Ref<number[]> = ref([]);

let radiations: number[] = [];
let radiations_view: Ref<number[]> = ref([]);

let winds: number[] = [];
let winds_view: Ref<number[]> = ref([]);
let wind_direction = ref(0);

let co2: {'benchmark': number[], 'decision': number[]} =
  {'benchmark': [], 'decision': []};
let co2_view: Ref<{'benchmark': number[], 'decision': number[]}> =
  ref({'benchmark': [], 'decision': []});

let money: Money[] = [];
let money_view: Ref<Money[]> = ref([]);

let demand: {"Fridge": Appliance[], "Lights": Appliance[], "ElectricHeater": Appliance[], "Total": Appliance[]} =
  {"Fridge": [], "Lights": [], "ElectricHeater": [], "Total": []};
let demand_view: Ref<{"Fridge": Appliance[], "Lights": Appliance[], "ElectricHeater": Appliance[], "Total": Appliance[]}> =
  ref({"Fridge": [], "Lights": [], "ElectricHeater": [], "Total": []});

let generation: {"SolarPanel": Generator[], "Windturbine": Generator[], "Total": Generator[]} =
  {"SolarPanel": [], "Windturbine": [], "Total": []};
let generation_view: Ref<{"SolarPanel": Generator[], "Windturbine": Generator[], "Total": Generator[]}> =
  ref({"SolarPanel": [], "Windturbine": [], "Total": []});

let battery_level: Energy[] = [];
let battery_level_view: Ref<Energy[]> = ref([]);

let grid: {"sold": Energy[], "bought": Energy[], "sell": Energy[], "buy": Energy[]} =
  {"sold": [], "bought": [], "sell": [], "buy": []};
let grid_view: Ref<{"sold": Energy[], "bought": Energy[], "sell": Energy[], "buy": Energy[]}> =
  ref({"sold": [], "bought": [], "sell": [], "buy": []});

let rotationX = 0;
let rotationY = 0;
let cubeColor = ref('hsl(90, 100%, 50%)');

const pause = defineModel();

let timer = -1
const lookback = 72

let lang = 'de'

onMounted(() => {
  /*
  let begin = new Date(2021, 0, 1, 0, 0, 0);
  let absolute_step = 0;
  console.log(begin);
  for (let i = 0; i < 3; i ++) {
    for (let j = 0; j < 365; j ++) {
      for (let k = 0; k < 144; k ++) {
        begin = addMinutes(begin, 10);
        // console.log(absolute_step, k, begin);
        absolute_step ++;
      }
    }
  }
  console.log("Ending", begin, absolute_step)
   */
  let chartsContainer = document.getElementsByClassName('singleChart');
  /*for (let chartContainer of chartsContainer) {
    chartContainer.firstChild.style.width = '';
  }
  onresize = (event) => {

  };*/
})

watch(currentIndex, async (newValue, oldValue) => {
})

watch(pause, async(newValue, oldValue) => {

})

watch(future, async(newValue, oldValue) => {

})

function pause_sim() {
  if (timer !== -1) {
    clearInterval(timer);
    timer = -1;
  }
}

function step() {
  currentIndex.value ++;
  simulate().then(res => {
    add_simulation_raw(res, true);
  });
}

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

function reset_sim() {
  dataFetched.value = false;
  reset_simulation().then();
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

function add_simulation_raw(res: Simulation, update: boolean) {
  let date = res['environment']['dates']
  current_time.value = date.toLocaleTimeString('de-DE')
  current_date.value = date.toLocaleDateString('de-DE')
  dates.push(date)
  future.value = date

  let precipitation = res['environment']['precipitations']
  precipitations.push(precipitation)

  let radiation = res['environment']['radiations']
  radiations.push(radiation)

  let temperature = res['environment']['temperatures']
  if (lang === 'de') {
    outside.value = temperature
  } else if (lang === 'en') {
    outside.value = temperature
  }
  temperatures.push(temperature)

  let wind = res['environment']['winds']
  wind_direction.value = res['environment']['wind_directions']
  winds.push(wind)

  let benchmark_inside_temperature = res['benchmark']['rooms'][2]['temperature']
  inside.value = benchmark_inside_temperature
  benchmark_inside_temperatures.push(benchmark_inside_temperature)
  show_cube_temperature(benchmark_inside_temperature.get_celsius())

  let decision_inside_temperature = res['decision']['rooms'][2]['temperature']
  decision_inside_temperatures.push(decision_inside_temperature)

  for (const algorithm of ['benchmark', 'decision']) {
    co2[algorithm as keyof Algorithms].push(res[algorithm as keyof Algorithms]['co2'])
  }

  let money_value = res['benchmark']['money']
  money.push(money_value)

  let total = new Appliance({ name: 'Total', 'demand': 0, 'usage': 0, 'on': false })
  for (const appliance of res['benchmark']['rooms'][2]['appliances']) {
    if (bob.includes(appliance.name as keyof IAppliances)) {
      demand[appliance['name'] as keyof IAppliances].push(appliance)
    }
    total.demand = total.demand.add(appliance.demand)
    total.usage = total.usage.add(appliance.usage)
  }
  demand['Total'].push(total)
  let total1 = new Generator({ name: 'Total', supply: 0, generation: 0 })
  for (const generator of res['benchmark']['generators']) {
    if (['SolarPanel', 'Windturbine'].includes(generator.name)) {
      generation[generator.name as keyof Generators].push(generator)
    }
    total1.supply = total1.supply.add(generator.supply)
    total1.generation = total1.generation.add(generator.generation)
  }
  generation['Total'].push(total1)
  let battery = res['benchmark']['battery']
  battery_level.push(battery.level)
  let grid_raw = res['benchmark']['grid']
  for (const gridParameter of ['sold', 'bought', 'sell', 'buy']) {
    grid[gridParameter as keyof IGrid].push(grid_raw[gridParameter as keyof IGrid])
  }

  if (update && currentIndex.value >= 3) {
    dataFetched.value = true
    let end = dates.length;
    let begin = Math.max(0, end - lookback) // only watch back 12h
    dates_view = dates.slice(begin, end)
    temperatures_view.value = temperatures.slice(begin, end)
    benchmark_inside_temperatures_view.value = benchmark_inside_temperatures.slice(begin, end)
    decision_inside_temperatures_view.value = decision_inside_temperatures.slice(begin, end)
    precipitations_view.value = precipitations.slice(begin, end)
    radiations_view.value = radiations.slice(begin, end)
    winds_view.value = winds.slice(begin, end)
    for (const applianceParameter of ['Fridge', 'Lights', 'ElectricHeater', 'Total']) {
      demand_view.value[applianceParameter as keyof IAppliances] = demand[applianceParameter as keyof IAppliances].slice(begin, end)
    }
    for (const generatorParameter of ['SolarPanel', 'Windturbine', 'Total']) {
      generation_view.value[generatorParameter as keyof Generators] = generation[generatorParameter as keyof Generators].slice(begin, end)
    }
    battery_level_view.value = battery_level.slice(begin, end)
    for (const gridParameter of ['sold', 'bought', 'sell', 'buy']) {
      grid_view.value[gridParameter as keyof IGrid] = grid[gridParameter as keyof IGrid].slice(begin, end)
    }
    for (const algorithm of ['benchmark', 'decision']) {
      co2_view.value[algorithm as keyof Algorithms] = co2[algorithm as keyof Algorithms].slice(begin, end)
    }
    money_view.value = money.slice(begin, end)
  }
}

const handleDate = (modelData: Date) => {
  // https://date-fns.org/v3.6.0/docs/differenceInMinutes
  let minuteDifference = differenceInMinutes(modelData, presetDates.value[0].value);
  if (minuteDifference > 0) {
    // console.log(minuteDifference)
    let absolute_step = minuteDifference / 10;
    // console.log(absolute_step)
    dataFetched.value = false;
    patch_future(absolute_step).then(res => {
      currentIndex.value = absolute_step;

      for (let i = 0; i < res.length - 1; i ++) {
        add_simulation_raw(res[i], false);
      }
      add_simulation_raw(res[res.length - 1], true);
      dataFetched.value = true;
    });
  }
}

/*
const filters = computed(() => {
  const currentDate = new Date(2021, 1, 1)
  return {
    months: Array.from(Array(3).keys())
      .map((item) => getMonth(addMonths(currentDate, item + 1)))
  }
})*/

function patch_outside() {
  patching().then(res => {
    console.log('Patch worked', res)
  });
}

function get_field(bucket, field: string, index: string) {
  return bucket[field].map<Energy>(item => item[index]);
}

</script>

<template>
  <div>
    <h1>Data</h1>
    <!--<p>{{start}}</p>
    <p>{{end}}</p>-->
    <!--<datepicker placeholder="Start Date" v-model="start" name="start-date"></datepicker>
    <datepicker placeholder="End Date" v-model="end" name="end-date"></datepicker>-->
    <!--<font-awesome-icon :icon="['fas', 'pause']" />-->
    <div>
      <v-btn class="mr-1" density="default" aria-label="Pause" icon="mdi-pause" :disabled="timer === -1" @click="pause_sim()"></v-btn>
      <v-btn class="mx-1" density="default" aria-label="Step" icon="mdi-step-forward" :disabled="timer !== -1" @click="step()"></v-btn>
      <v-btn class="mx-1" density="default" aria-label="Play" icon="mdi-play" :disabled="timer !== -1" @click="play()"></v-btn>
      <v-btn class="mx-1" density="default" aria-label="Fast" icon="mdi-fast-forward" :disabled="timer !== -1" @click="fast()"></v-btn>
      <v-btn class="ml-1" density="default" aria-label="Reset" icon="mdi-replay" @click="reset_sim()"></v-btn>
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
    <div>
      <VueDatePicker
        v-model="future"
        @update:model-value="handleDate"
        :preset-dates="presetDates"
        no-today
        :loading="!dataFetched"
        :min-date="presetDates[0].value"
        :max-date="presetDates[2].value"
        minutes-increment="10"
        minutes-grid-increment="10"
        select-text="Auswählen"
        cancel-text="Abbrechen">
          <!--locale="de"
          :filter="filter"
          :is-24="false"
          https://vue3datepicker.com/props/localization/-->
      </VueDatePicker>
    </div>
  </div>
  <div class="controls" v-if="dataFetched">
    <input type="range" min="0" :max="lookback" value="0" v-model="currentIndex" />
  </div>
  <div class="overrides mb-16">
    <v-btn density="default" icon="mdi-sun-thermometer-outline" @click="patch_outside()"></v-btn>
  </div>
  <div>
    <div class="charts">
      <div class="singleChart">
        <LinesChart v-if="dataFetched"
                    id="co2_plot"
                    :key="currentIndex"
                    :keys="dates_view"
                    :axes="['Benchmark CO2', 'Decision CO2']"
                    :values="[co2_view['benchmark'], co2_view['decision']]"/>
      </div>
      <div class="singleChart">
        <LinesChart v-if="dataFetched"
                    id="temperature_plot"
                    :key="currentIndex"
                    :keys="dates_view"
                    :axes="['Outside Temperature', 'Benchmark Inside Temperature', 'Decision Inside Temperature']"
                    :values="[temperatures_view, benchmark_inside_temperatures_view, decision_inside_temperatures_view]"/>
      </div>
      <div class="singleChart">
        <LinesChart v-if="dataFetched"
                    id="precipitation_plot"
                    :key="currentIndex"
                    :keys="dates_view"
                    :axes="['Precipitation']"
                    :values="[precipitations_view]"/>
      </div>
      <div class="singleChart">
        <LinesChart v-if="dataFetched"
                    id="radiation_plot"
                    :key="currentIndex"
                    :keys="dates_view"
                    :axes="['Radiation']"
                    :values="[radiations_view]"/>
      </div>
      <div class="singleChart">
        <LinesChart v-if="dataFetched"
                    id="solar_plot"
                    :key="currentIndex"
                    :keys="dates_view"
                    :axes="['Solar generation', 'Windturbine generation', 'Total']"
                    :values="[get_field(generation_view, 'SolarPanel', 'supply'),
                      get_field(generation_view, 'Windturbine', 'supply'),
                      get_field(generation_view, 'Total', 'supply')]"/>
      </div>
      <div class="singleChart">
        <LinesChart v-if="dataFetched"
                    id="battery_plot"
                    :key="currentIndex"
                    :keys="dates_view"
                    :axes="['Battery Level']"
                    :values="[battery_level_view]"/>
      </div>
      <div class="singleChart">
        <LinesChart v-if="dataFetched"
                    id="wind_plot"
                    :key="currentIndex"
                    :keys="dates_view"
                    :axes="['Wind']"
                    :values="[winds_view]"/>
      </div>
      <div class="singleChart">
        <WindComponent v-if="dataFetched"
                       id="wind_direction"
                       :key="currentIndex"
                       :keys="dates_view"
                       :axes="'Wind direction'"
                       :values="wind_direction"/>
      </div>
      <div class="singleChart">
        <LinesChart v-if="dataFetched"
                    id="appliances_plot"
                    :key="currentIndex"
                    :keys="dates_view"
                    :axes="['Fridge', 'Lights', 'ElectricHeater', 'Total']"
                    :values="[get_field(demand_view, 'Fridge', 'demand'),
                      get_field(demand_view, 'Lights', 'demand'),
                      get_field(demand_view, 'ElectricHeater', 'demand'),
                      get_field(demand_view, 'Total', 'demand')]"/>
      </div>
      <div class="singleChart">
        <LinesChart v-if="dataFetched"
                    id="money_plot"
                    :key="currentIndex"
                    :keys="dates_view"
                    :axes="['Money']"
                    :values="[money_view]"/>
      </div>
      <div class="singleChart">
        <LinesChart v-if="dataFetched"
                    id="grid_plot"
                    :key="currentIndex"
                    :keys="dates_view"
                    :axes="['Grid bought', 'Grid sold']"
                    :mode="'Mode.KILO_WATT_HOURS'"
                    :values="[grid_view['bought'], grid_view['sold']]"/>
      </div>
      <div class="singleChart">
        <LinesChart v-if="dataFetched"
                    id="grid_cur_plot"
                    :key="currentIndex"
                    :keys="dates_view"
                    :axes="['Grid buying', 'Grid selling']"
                    :values="[grid_view['buy'], grid_view['sell']]"/>
      </div>
      <div class="singleChart">
        <LinesChart v-if="dataFetched"
                    id="sum_generators"
                    :key="currentIndex"
                    :keys="dates_view"
                    :axes="['Solar generation', 'Windturbine generation', 'Total']"
                    :mode="'Mode.KILO_WATT_HOURS'"
                    :values="[get_field(generation_view, 'SolarPanel', 'generation'),
                      get_field(generation_view, 'Windturbine', 'generation'),
                      get_field(generation_view, 'Total', 'generation')]"/>
      </div>
      <div class="singleChart">
        <LinesChart v-if="dataFetched"
                    id="sum_appliances"
                    :key="currentIndex"
                    :keys="dates_view"
                    :axes="['Fridge', 'Lights', 'ElectricHeater', 'Total']"
                    :mode="'Mode.KILO_WATT_HOURS'"
                    :values="[get_field(demand_view, 'Fridge', 'usage'),
                      get_field(demand_view, 'Lights', 'usage'),
                      get_field(demand_view, 'ElectricHeater', 'usage'),
                      get_field(demand_view, 'Total', 'usage')]"/>
      </div>
    </div>
    <p v-if="!dataFetched">Loading...</p>
  </div>
  <div class="stats mt-16">
    <div>
      Outside temperature:
      <div class="font-weight-bold d-inline">{{outside.format_celsius()}}</div>
    </div>
    <div>
      Inside temperature:
      <div class="font-weight-bold d-inline">{{inside.format_celsius()}}</div>
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

.charts {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
}

.singleChart {
  flex-grow: 0;
  flex-shrink: 0;
  width: 45vw;
}
</style>
