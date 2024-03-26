<template>
  <div class="stats">
    <div>
      Outside temperature:
      <div>{{outside}}</div>
    </div>
    <div>
      Inside temperature:
      <div>{{inside}}</div>
    </div>
  </div>
  <div class="controls">
    <input type="range" min="0" max="100" value="0" v-model="cubeColor" />
  </div>
  <div class="cube-container">
    <div class="cube">
      <div class="face front">Front</div>
      <div class="face back">Back</div>
      <div class="face left">Left</div>
      <div class="face right">Right</div>
      <div class="face top">Top</div>
      <div class="face bottom">Bottom</div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      rotationX: 0,
      rotationY: 0,
      cubeColor: 'hsl(90, 100%, 50%)',
      outside: 11,
      inside: 21
    };
  },
  watch: {
    cubeColor(time) {
      let heat = calculateHeat(time, this.inside, this.outside)
      let color = toColor(heat)
      let children = document.querySelector(".cube").children
      for (const child of children) {
        child.style.backgroundColor = `hsl(${color}, 100%, 50%)`;
      }
    },
  },
};

function calculateHeat(time, inside, outside) {
  let temperature = inside
  for (let i = 0; i < time; i++) {
    let delta = (outside - temperature) * 0.1
    temperature += delta
  }
  return temperature
}

function map(x, in_min, in_max, out_min, out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

function toColor(heat) {
  return map(heat, 0, 30, 180, 0)
}
</script>

<style scoped>
.cube-container {
  perspective: 1000px;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.cube {
  width: 100px;
  height: 100px;
  position: relative;
  transform-style: preserve-3d;
  transition: transform 0.5s;
  transform: rotateX(-25deg) rotateY(45deg);
}

.face {
  position: absolute;
  width: 100px;
  height: 100px;
  border: 1px solid #000;
  opacity: 0.8;
  background-color: hsl(0, 100%, 50%);
}

.front {
  transform: rotateY(0deg) translateZ(50px);
}

.back {
  transform: rotateY(180deg) translateZ(50px);
}

.left {
  transform: rotateY(-90deg) translateZ(50px);
}

.right {
  transform: rotateY(90deg) translateZ(50px);
}

.top {
  transform: rotateX(90deg) translateZ(50px);
}

.bottom {
  transform: rotateX(-90deg) translateZ(50px);
}

input[type="range"] {
  width: 100%;
  margin-top: 20px;
}
</style>