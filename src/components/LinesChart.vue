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

const colors = ["#f87979", "#79f879", "#7979f8"];

export default {
  name: 'LineChart',
  components: {
    // eslint-disable-next-line vue/no-reserved-component-names
    Line
  },
  props: ['keys', 'axes', 'values'],
  data() {
    return {
      data: {
        labels: this.keys.map((date: Date) => {
          return date.toLocaleTimeString('de-DE', {timeStyle: 'short'})
        }),
        datasets: transformData(this.axes, this.values),
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
          y: {
            min: 0,
            max: 35,
            suggestedMin: 0,
            suggestedMax: 35
          }
        },
        animation: false,
      },
    }
  },
  setup(props) {
    // console.log('KEYS', props.keys);
    // console.log('VALUES', props.values);
  },

}

function transformData(axes: string[], values: [number[]]): {'label': string, 'backgroundColor': string, data: number[]}[] {
  let data = [];
  if (axes.length !== values.length) {
    console.error('Axes does not match values length', axes, values);
  }
  for (let i = 0; i < values.length; i++) {
    data.push({
      label: axes[i],
      backgroundColor: colors[i % colors.length],
      data: values[i]
    });
  }
  // console.log('Multiple Axis Data', data)
  return data;
  /*return [
          {
            label: 'Temperature',
            backgroundColor: '#f87979',
            data: this.values,
          }
        ];*/
}
</script>
