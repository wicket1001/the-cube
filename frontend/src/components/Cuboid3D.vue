<script setup lang="ts">

</script>

<template>
  <div class="cuboid">
    <div class="side"></div>
    <div class="side"></div>
    <div class="side"></div>
    <div class="side"></div>
    <div class="side"></div>
    <div class="side"></div>
  </div>
</template>

<style scoped>

.cuboid {
	--height: 2;
  --width: 2;
  --depth: 2;
	--hue: 200;
	--sat: 10%;
	height: calc(var(--height) * 1vmin);
	width: calc(var(--width) * 1vmin);
	position: absolute;
	animation: cube1 0.6s linear 0s infinite;
	transform: translate3d(0vmin, 0vmin, -5vmin);
}

.cuboid .side {
	position: absolute;
	top: 50%;
	left: 50%;
	height: 100%;
	width: 100%;
	border-radius: 2px;
	background: hsl(var(--hue), var(--sat), 10%);
}

.cuboid .side:nth-of-type(1) {
	transform: translate3d(-50%, -50%, calc(var(--depth) * 0.5vmin));
	filter: brightness(0.75);
}
.cuboid .side:nth-of-type(2) {
	transform: translate3d(-50%, -50%, calc(var(--depth) * -0.5vmin)) rotateY(180deg);
}
.cuboid .side:nth-of-type(3) {
	width: calc(var(--depth) * 1vmin);
	transform: translate(-50%, -50%) rotateY(90deg)	translate3d(0, 0, calc(var(--width) * 0.5vmin));
	filter: brightness(1.5);
}
.cuboid .side:nth-of-type(4) {
	width: calc(var(--depth) * 1vmin);
	transform: translate(-50%, -50%) rotateY(-90deg) translate3d(0, 0, calc(var(--width) * 0.5vmin));
	filter: brightness(0.6);
}
.cuboid .side:nth-of-type(5) {
	height: calc(var(--depth) * 1vmin);
	transform: translate(-50%, -50%) rotateX(90deg)	translate3d(0, 0, calc(var(--height) * 0.5vmin));
	filter: brightness(2);
}
.cuboid .side:nth-of-type(6) {
	height: calc(var(--depth) * 1vmin);
	transform: translate(-50%, -50%) rotateX(-90deg) translate3d(0, 0, calc(var(--height) * 0.5vmin));
	filter: brightness(1.25);
}

.side:before {
  content: "";
  position: absolute;
  width: 100%;
  height: 100%;
  --units: 0.25vmin;
  --brick1: #ef490d;
  --brick2: #f13500;
  --lines: #5e5e5e;
	--brick1: #724f42;
  --brick2: #795548;
  --lines: #9b8989;

  --gp-ln: 50%/ calc(var(--units) * 10) calc(var(--units) * 5);
  --gp-cn: 50%/ calc(var(--units) * 5) calc(var(--units) * 5);
  background: repeating-conic-gradient(from 90deg at 95% 55%, var(--lines) 0% 25%, #fff0 0% 100%) var(--gp-cn), repeating-linear-gradient(180deg, var(--lines) 0 5%, #fff0 0 50%, var(--lines) 0 55%, var(--brick2) 0 100% ) var(--gp-ln), repeating-linear-gradient(90deg, var(--brick1) 0 47.5%, var(--lines) 0 50%, var(--brick1) 0 97.5%, var(--lines) 0 100% ) var(--gp-ln);
  opacity: 0.5;
}
</style>