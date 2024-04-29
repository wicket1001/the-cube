<script setup lang="ts">

</script>

<template>
  <div class="panel">
    <div class="base">

    </div>
    <div class="shaft">

    </div>
    <div class="solarcell">

    </div>
  </div>
</template>

<style scoped>
.panel {
  position: absolute;
  /*width: calc(var(--side-length) / 4);
  height: calc(var(--side-length) / 4);*/
  /*border: 1px solid #000;*/
  transform: rotateX(90deg) translateZ(calc(var(--side-length) / 2));
}

.solarcell {
  width: calc(var(--side-length) / 4);
  height: calc(var(--side-length) / 4);
  background-color: rgb(0, 0, 255);
  border-bottom: black 1px solid;
  border-right: black 1px solid;
}
</style>