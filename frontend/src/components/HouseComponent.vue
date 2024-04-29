<script setup lang="ts">

import Cuboid3D from '@/components/Cuboid3D.vue'
</script>

<template>
  <Cuboid3D class="house"/>
  <Cuboid3D class="house-roof"/>
</template>

<style scoped>
.house {
  --width: 7;
  --height: 9;
  --depth: 12;
  transform: translate3d(-23vmin, 20.85vmin, 11.5vmin);
}
.house >>> .side:nth-of-type(1) {
    clip-path: polygon(0% 0%, 0% 100%, 50% 100%, 50% 32%, 90% 32%, 90% 85%, 50% 85%, 50% 100%, 100% 100%, 100% 0%);
}
.house >>> .side:nth-of-type(3):after {
    content: "";
    background: #00000069;
    width: 1.2vmin;
    height: 1.2vmin;
    position: absolute;
    left: 59%;
    top: 18%;
    border-radius: 100%;
    border-left: 1px solid #fff8;
    box-sizing: border-box;
}

/*** ROOF ***/
.house-roof {
	--width: 6;
    --height: 6;
    --depth: 13;
    transform: translate3d(-23vmin, 16.85vmin, 11.5vmin) rotate(45deg);
}
.house-roof >>> .side {
	background: red;
}
.house-roof >>> .side:nth-child(1) {
	clip-path: polygon(0 0, 100% 0%, 0% 100%);
	background: #181818;
	transform: translate3d(-50%, -50%, calc(var(--depth) * 0.46vmin));
}
.house-roof >>> .side:nth-child(2) {
	clip-path: polygon(0 0, 100% 100%, 100% 0);
	background: #181818;
	transform: translate3d(-50%, -50%, calc(var(--depth) * -0.46vmin)) rotateY(180deg);
}
.house >>> .side:nth-child(5),
.house-roof >>> .side:nth-child(3),
.house-roof >>> .side:nth-child(6) {
	opacity: 0;
}

.house-roof >>> .side:nth-child(1):before,
.house-roof >>> .side:nth-child(2):before {
    transform: rotate(-45deg);
    width: 200%;
    height: 200%;
    top: -50%;
    left: -50%;
}
.house-roof >>> .side:nth-child(2):before {
    transform: rotate(45deg);
}
.house-roof >>> .side:nth-child(4){
    overflow: hidden;
}
.house-roof >>> .side:nth-child(4):before {
    transform: rotate(90deg) translate(-7vmin, 0vmin);
    height: 15vmin;
}

</style>