import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

/*
import { useCounterStore } from '@/stores/counter'

const counter = useCounterStore()



<div>
  <p>Count: {{counter.count}}</p>
  <p>Double Count: {{counter.doubleCount}}</p>
  <button @click="counter.increment()">Increemtn</button>
</div>
 */

export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  const doubleCount = computed(() => count.value * 2)
  function increment() {
    count.value++
  }

  return { count, doubleCount, increment }
})
