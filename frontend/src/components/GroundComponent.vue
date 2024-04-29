<script setup lang="ts">

import Cuboid3D from '@/components/Cuboid3D.vue'
</script>

<template>
  <Cuboid3D class="ground"/>
</template>

<style scoped>
.ground {
  --width: 58;
  --depth: 58;
  --height: 4;
  transform: translateY(27.8vmin);
}

.ground >>> .side {
  background-color: #193c11;
}

.ground >>> .side:before {
  opacity: 0.35;
}
</style>