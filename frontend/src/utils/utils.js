
export function calculateHeat(time, inside, outside) {
  let temperature = inside
  for (let i = 0; i < time; i++) {
    let delta = (outside - temperature) * 0.1
    temperature += delta
  }
  return temperature
}

export function stepHeat(time, inside, outside) {
  let delta = (outside - inside) * 0.1;
  return inside + delta;
}

export function mapping(x, in_min, in_max, out_min, out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

export function toColor(heat) {
  return mapping(heat, 0, 30, 180, 0)
}
