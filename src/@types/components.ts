import { Energy } from '@/@types/physics'


export class Appliance implements IAppliance {
  "name": string;
  "demand": Energy;
  "usage": Energy;
  "on": boolean;

  constructor({name, demand, usage, on}: {name: string, demand: number, usage: number, on: boolean}) {
    this.name = name;
    this.demand = new Energy(demand);
    this.usage = new Energy(usage);
    this.on = on;
  }
}
export interface IAppliance {
  "name": string,
  "demand": Energy,
  "usage": Energy,
  "on": boolean
}

export class Generator implements IGenerator {
  "name": string;
  "supply": Energy;
  "generation": Energy;

  constructor({name, supply, generation}: {name: string, supply: number, generation: number}) {
    this.name = name;
    this.supply = new Energy(supply);
    this.generation = new Energy(generation);
  }
}
export interface IGenerator {
  "name": string,
  "supply": Energy,
  "generation": Energy
}

export class Battery implements IBattery {
  "level": Energy;
  "stored": Energy;
  "taken": Energy;

  constructor({level, stored, taken}: {level: number, stored: number, taken: number}) {
    this.level = new Energy(level);
    this.stored = new Energy(stored);
    this.taken = new Energy(taken);
  }
}
export interface IBattery {
  "level": Energy,
  "stored": Energy,
  "taken": Energy
}
