import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { MutationType } from 'pinia'

export const useGlobalStorage = defineStore('storage', () => {
  const battery = ref(0)
  const money = ref(0)


  const INITIAL_HEAT = 21;
  let currentIndex = ref(0);



  return {currentIndex}
})
