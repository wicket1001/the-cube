<template>
  <div class="cube-container">
    <div class="cube" :style="{ transform: `rotateX(${rotationX}deg) rotateY(${rotationY}deg)` }">
      <div class="face front" :style="{ backgroundColor: cubeColor }"></div>
      <div class="face back" :style="{ backgroundColor: cubeColor }"></div>
      <div class="face left" :style="{ backgroundColor: cubeColor }"></div>
      <div class="face right" :style="{ backgroundColor: cubeColor }"></div>
      <div class="face top" :style="{ backgroundColor: cubeColor }"></div>
      <div class="face bottom" :style="{ backgroundColor: cubeColor }"></div>
    </div>
    <input type="range" v-model="cubeColor" />
  </div>
</template>

<script>
export default {
  data() {
    return {
      rotationX: 0,
      rotationY: 0,
      cubeColor: "#ff0000", // Initial color (red)
    };
  },
  watch: {
    cubeColor(newColor) {
      // Update cube color when slider value changes
      console.log(newColor)
      console.log(this.$el.querySelector(".cube"))
      this.$el.querySelector(".cube").style.backgroundColor = `hsl(${newColor}, 100%, 100%)`;
    },
  },
};
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
}

.face {
  position: absolute;
  width: 100px;
  height: 100px;
  border: 1px solid #000;
  opacity: 0.8;
}

.front {
  transform: translateZ(50px);
}

.back {
  transform: translateZ(-50px) rotateY(180deg);
}

.left {
  transform: rotateY(-90deg) translateX(-50px);
}

.right {
  transform: rotateY(90deg) translateX(50px);
}

.top {
  transform: rotateX(90deg) translateY(-50px);
}

.bottom {
  transform: rotateX(-90deg) translateY(50px);
}

input[type="range"] {
  width: 100%;
  margin-top: 20px;
}
</style>