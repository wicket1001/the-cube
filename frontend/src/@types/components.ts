import { Energy } from '@/@types/physics'


export class Appliance {
  "name": string;
  "demand": Energy;
  "usage": Energy;
  "on": boolean;

  constructor({name, demand, usage, on}: IAppliance) {
    this.name = name;
    this.demand = new Energy(demand);
    this.usage = new Energy(usage);
    this.on = on;
  }
}
export interface IAppliance {
  "name": string,
  "demand": number,
  "usage": number,
  "on": boolean
}

export class Generator {
  "name": string;
  "supply": Energy;
  "generation": Energy;

  constructor({name, supply, generation}: IGenerator) {
    this.name = name;
    this.supply = new Energy(supply);
    this.generation = new Energy(generation);
  }
}
export interface IGenerator {
  "name": string,
  "supply": number,
  "generation": number
}

export class Battery {
  "level": Energy;
  "stored": Energy;
  "taken": Energy;

  constructor({level, stored, taken}: IBattery) {
    this.level = new Energy(level);
    this.stored = new Energy(stored);
    this.taken = new Energy(taken);
  }
}
export interface IBattery {
  "level": number,
  "stored": number,
  "taken": number
}

export class Grid {
  "sold": Energy;
  "bought": Energy;
  "sell": Energy;
  "buy": Energy;

  constructor({sold, bought, sell, buy}: IGrid) {
    this.sold = new Energy(sold);
    this.bought = new Energy(bought);
    this.sell = new Energy(sell);
    this.buy = new Energy(buy);
  }
}
export interface IGrid {
  "sold": number,
  "bought": number,
  "sell": number,
  "buy": number
}
