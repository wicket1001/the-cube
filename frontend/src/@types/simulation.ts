import type { IAppliance, IBattery, IGenerator, IGrid } from '@/@types/components'
import { Appliance, Battery, Generator, Grid } from '@/@types/components'

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
    IAppliance
  ],
  "generators": [
    IGenerator
  ],
  "battery": IBattery,
  "grid": IGrid
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
    Appliance
  ],
  "generators": [
    Generator
  ],
  "battery": Battery,
  "grid": Grid
}