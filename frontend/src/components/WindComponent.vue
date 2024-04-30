<template>
  <Doughnut :data="data" :options="options" />
</template>

<script lang="ts">
import {
  ArcElement,
  CategoryScale,
  Chart as ChartJS,
  DoughnutController,
  Legend,
  LinearScale,
  Title,
  Tooltip

} from 'chart.js'
import { Doughnut } from 'vue-chartjs'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  DoughnutController,
  ArcElement
)

export default {
  name: 'WindChart',
  components: {
    Doughnut
  },
  props: ['keys', 'axes', 'values'],
  data() {
    return {
      data: {
        labels: [
          this.axes,
        ],
        datasets: [{
          label: 'Wind',
          data: [10, 350],
          backgroundColor: [
            "#7979f8",
            'rgba(54, 162, 235, 0)',
          ],
          hoverOffset: 4,
          rotation: (this.values + 355)
        }]
      },
      options: {
        aspectRatio: 2,
        responsive: true,
        animation: false
      }
    }
  },
  setup(props) {

  }
}

</script>

<style scoped>

</style>