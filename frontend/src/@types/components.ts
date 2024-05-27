import { Energy, Money, Temperature } from '@/@types/physics'

export class Algorithm {
  "co2": number;
  "money": Money;
  "battery": Battery;
  "grid": Grid;
  "generators": Generator[];
  "rooms": Room[];

  constructor({co2, money, battery, grid, generators, rooms}: IAlgorithm) {
    this.co2 = co2;
    this.money = new Money(money);
    this.battery = new Battery(battery);
    this.grid = new Grid(grid);
    this.generators = [];
    this.rooms = [];
    for (const generator of generators) {
      this.generators.push(new Generator(generator));
    }
    for (const room of rooms) {
      this.rooms.push(new Room(room));
    }
  }
}
export interface IAlgorithm {
  "co2": number,
  "money": number,
  "battery": IBattery,
  "grid": IGrid,
  "generators": [
    IGenerator
  ],
  "rooms": [
    IRoom
  ]
}

export class Environment {
  "dates": Date;
  "radiations": number;
  "temperatures": Temperature;
  "winds": number;
  "wind_directions": number;

  constructor({dates, radiations, temperatures, winds, wind_directions}: IEnvironment) {
    this.dates = new Date(dates);
    this.radiations = radiations;
    this.temperatures = new Temperature(temperatures);
    this.winds = winds;
    this.wind_directions = wind_directions;
  }
}
export interface IEnvironment {
  "dates": string,
  "radiations": number,
  "temperatures": number,
  "winds": number,
  "wind_directions": number,
}

export class Room {
  "name": string;
  "temperature": Temperature;
  "appliances": Appliance[];

  constructor({name, temperature, appliances}: IRoom) {
    this.name = name;
    this.temperature = new Temperature(temperature);
    this.appliances = [];
    for (const appliance of appliances) {
      this.appliances.push(new Appliance(appliance));
    }
  }
}
export interface IRoom {
  "name": string,
  "temperature": number,
  "appliances": [
    IAppliance
  ],
}

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
