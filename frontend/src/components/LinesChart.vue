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
import { Energy, Money, Temperature } from '@/@types/physics'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

const colors = ["#f87979", "#79f879", "#7979f8", "#f7f679", "#7984f7"];
// const colors = ["#36a2eb", "#ff6384", "#4bc0c0", "#ff9f40", "#9966ff", "#ffcd56", "#c9cbcf"];

export default {
  name: 'LineChart',
  components: {
    // eslint-disable-next-line vue/no-reserved-component-names
    Line
  },
  props: ['keys', 'axes', 'values', 'mode'],
  data() {
    return {
      data: {
        labels: this.keys.map((date: Date) => {
          return date.toLocaleTimeString('de-DE', {timeStyle: 'short'})
        }),
        datasets: transformData(this.axes, this.values, this.mode),
      },
      options: {
        //responsive: true,
        //maintainAspectRatio: true,
        aspectRatio: 2,
        responsive: true,
        scales: {
          y: {
            suggestedMin: 0,
            suggestedMax: 35,
            ticks: {
              callback: formatAxis
            }
          }
        },
        animation: false,
        /*resizeDelay: 0,
        transitions: {
          active: {
            animation: {
              duration: 0
            }
          }
        }*/
        plugins: {
          legend: {
            display: true,
            position: 'bottom'
          }
        }
      },
    }
  },
  setup(props) {

  },

}

let formatAxis = function(value: number) {
  return `${value}`;
}

function transformData(axes: string[], values: [number[] | Energy[] | Money[]], mode: string): {'label': string, 'backgroundColor': string, data: number[]}[] {
  let data = [];
  if (axes.length !== values.length) {
    console.error('Axes does not match values length', axes, values);
  }
  for (let i = 0; i < values.length; i++) {
    data.push({
      label: axes[i],
      backgroundColor: colors[i % colors.length],
      data: values[i].map<number>(item => {
          if (typeof item === 'number') {
            formatAxis = function(value: number) {
              return `${value}`;
            }
            return item;
          } else if (item instanceof Energy) {
            if (mode && mode === 'Mode.KILO_WATT_HOURS') {
              formatAxis = function(value: number) {
                return `${value} kWh`;
              }
              return item.get_kilo_watt_hours();
            } else {
              formatAxis = function(value: number) {
                return `${value} Wh`;
              }
              return item.get_watt_hours();
            }
          } else if (item instanceof Money) {
            formatAxis = function(value: number) {
              return `${value} €`;
            }
            return item.value;
          } else if (item instanceof Temperature) {
            formatAxis = function(value: number) {
              return `${value} °C`;
            }
            return item.get_celsius();
          } else {
            console.error('In transformData.map occured an error.', item);
            return item;
          }
        }
      )
    });
  }
  return data;
}
</script>
