<template>
  <Line :data="data" :options="options" />
</template>

<script lang="ts">
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import { Line } from 'vue-chartjs'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

export default {
  name: 'LineChart',
  components: {
    // eslint-disable-next-line vue/no-reserved-component-names
    Line
  },
  props: ['keys', 'values'],
  data() {
    return {
      data: {
        labels: this.keys.map((date: Date) => {
          return date.toLocaleTimeString('de-DE', {timeStyle: 'short'})
        }),
        datasets: [
          {
            label: 'Temperature',
            backgroundColor: '#f87979',
            data: this.values,
          }
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
      }
    }
  },
  setup(props) {
    console.log(props.keys);
    console.log(props.values);
  },

}
</script>
