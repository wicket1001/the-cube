export interface SimulationRaw {
  "step": number,
  "absolute_step": number,
  "environment": {
    "dates": string,
    "radiations": number,
    "temperatures": number,
    "winds": number,
    "wind_directions": number,
    "inner_temperature": number,
    "money": number
  },
  "appliances": [
    {
      "name": string,
      "demand": number,
      "usage": number,
      "on": boolean
    }
  ],
  "generators": [
    {
      "name": string,
      "supply": number,
      "generation": number
    }
  ],
  "battery": {
    "level": number,
    "stored": number,
    "taken": number
  },
  "grid": {
    "sold": number,
    "bought": number,
    "sell": number,
    "buy": number
  }
}

export interface Simulation {
  "step": number,
  "absolute_step": number,
  "environment": {
    "dates": Date,
    "radiations": number,
    "temperatures": number,
    "winds": number,
    "wind_directions": number,
    "inner_temperature": number,
    "money": number
  },
  "appliances": [
    {
      "name": string,
      "demand": number,
      "usage": number,
      "on": boolean
    }
  ],
  "generators": [
    {
      "name": string,
      "supply": number,
      "generation": number
    }
  ],
  "battery": {
    "level": number,
    "stored": number,
    "taken": number
  }
}