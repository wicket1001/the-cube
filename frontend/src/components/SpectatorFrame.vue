<script setup lang="ts">

import Cuboid from '@/components/Cuboid3D.vue'
import HouseComponent from '@/components/HouseComponent.vue'
import GroundComponent from '@/components/GroundComponent.vue'
</script>

<template>
  <div class="all">
    <div class="body-wrapper">
      <div class="scene">
        <div class="content">
          <HouseComponent/>
          <GroundComponent/>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.all {
  transform-style: preserve-3d;
	box-sizing: border-box;

}

.body-wrapper {
  margin: 0;
	padding: 0;
	width: 100vw;
	height: 100vh;
	overflow: hidden;
	display: flex;
	align-items: center;
	justify-content: center;
	perspective: 1000vmin;
	background: radial-gradient(circle at 50% 50%, #333, #021320);
	cursor: zoom-in;
}

.body-wrapper:active .scene {
  transform: scale3d(1.35, 1.35, 1.35);
  transition: all 1s ease 0s;
}

.scene {
  width: 50vmin;
  height: 50vmin;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 1s ease 0s;
}


.content {
	width: 50vmin;
  height: 50vmin;
  display: flex;
  align-items: center;
  justify-content: center;
  transform: rotateX(-27.25deg) rotateY(-48.75deg) rotateZ(0deg);
	transition: all 1s ease 0s;
  margin-top: -20vmin;
	animation: back-scene 1s linear 0s 1;
}

.content:hover {
	animation: spin-scene 20s linear 0s infinite;
}

@keyframes spin-scene {
	0% { transform: rotateX(-27.25deg) rotateY(-48.75deg) rotateZ(0deg); }
	100% { transform: rotateX(-27.25deg) rotateY(-408.75deg) rotateZ(0deg); }
}

@keyframes back-scene {
	0%, 100% { transform: rotateX(-27.25deg) rotateY(-48.75deg) rotateZ(0deg); }
	25% { transform: rotateX(-27.25deg) rotateY(-52.75deg) rotateZ(0deg); }
	50% { transform: rotateX(-27.25deg) rotateY(-46.75deg) rotateZ(0deg); }
	75% { transform: rotateX(-27.25deg) rotateY(-49.75deg) rotateZ(0deg); }
}

.body-wrapper:active .content {
	animation-play-state: paused;
}

.content:before {
  content: "";
  position: absolute;
  width: calc(100% + 4vmin);
  height: calc(100% + 4vmin);
  background: green;
  transform: rotateX(90deg) translateZ(-25.5vmin);
  border-radius: 1vmin;
  box-shadow: 0 0 1vmin 0 #0008 inset;
  background:
  radial-gradient(#1c8820 12%, transparent 18%) 0px 0,
  radial-gradient(#4caf5080 12%, transparent 18%) 3px 4px,
  radial-gradient(#ffffff40 12%, transparent 23%) 0 1px,
  radial-gradient(#ffffff30 12%, transparent 23%) 2px 3px;
  background-color: #298f2c;
  background-size: 5px 4px;
}
</style>