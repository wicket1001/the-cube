import { ref, computed, reactive } from 'vue'
import { type Ref } from 'vue';
import { defineStore } from 'pinia'
import { MutationType } from 'pinia'

export const useGlobalStorage = defineStore('storage', () => {
  const battery = ref(0)
  const money = ref(0)


  const INITIAL_HEAT = 21;

  let currentIndex = ref(0);
  // let current = ref('');
  let outside = ref(0);
  let inside = ref(INITIAL_HEAT);
  let dataFetched: Ref<boolean> = ref(false); // : Ref<boolean>
  let playBtn = ref('Play')

  let dates: Date[] = reactive([]);
  let dates_view: Date[] = reactive([]); // : Ref<Date[]>

  let temperatures = reactive([] as number[]);
  let temperatures_view: number[] = reactive([]); // : Ref<number[]>

  let inside_temperatures: number[] = reactive([]);
  let inside_temperatures_view: number[] = reactive([]); // : Ref<number[]>

  const current = computed(() => {
    console.log(dates)
    console.log(currentIndex.value)
    if (dates.length <= 0) {
      return '';
    }
    return dates[currentIndex.value].toLocaleTimeString()
  });

  return {currentIndex, current, outside, inside, dataFetched, playBtn, dates, dates_view,
          temperatures, temperatures_view, inside_temperatures, inside_temperatures_view}
})
