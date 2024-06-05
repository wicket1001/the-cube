import { Energy, Money, Temperature } from '@/@types/physics'

export class Algorithms {
  "benchmark": Algorithm;
  "decision": Algorithm;
}
export interface IAlgorithms extends Algorithms {}
export type TAlgorithms = Array<keyof IAlgorithms>;
export const algorithms_named: TAlgorithms = Object.keys(new Algorithms()) as TAlgorithms;

export class Algorithm {
  "co2": number;
  "money": Money;
  "battery": Battery;
  "grid": Grid;
  "generators": Generator[];
  "rooms": Room[];
  "HeatPump": Appliance;

  constructor({co2, money, battery, grid, generators, rooms, HeatPump}: IAlgorithm) { // appliances
    this.co2 = co2;
    this.money = new Money(money);
    this.battery = new Battery(battery);
    this.grid = new Grid(grid);
    this.generators = [];
    this.rooms = [];
    this.HeatPump = new Appliance(HeatPump);
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
  ],
  "HeatPump": IAppliance
}

export class Environment {
  "dates": Date;
  "radiations": number;
  "precipitations": number;
  "temperatures": Temperature;
  "winds": number;
  "wind_directions": number;

  constructor({dates, radiations, precipitations, temperatures, winds, wind_directions}: IEnvironment) {
    this.dates = new Date(dates);
    this.radiations = radiations;
    this.precipitations = precipitations;
    this.temperatures = new Temperature(temperatures);
    this.winds = winds;
    this.wind_directions = wind_directions;
  }
}
export interface IEnvironment {
  "dates": string,
  "radiations": number,
  "precipitations": number,
  "temperatures": number,
  "winds": number,
  "wind_directions": number,
}

export class Rooms {
  'Cellar left': Room;
  'Cellar right': Room;
  'First left': Room;
  'First right': Room;
  'Second left': Room;
  'Second right': Room;
  'Third left': Room;
  'Third right': Room;
  'Attic left': Room;
  'Attic right': Room;
}
export interface IRooms extends Rooms {}
export type TRooms = Array<keyof IRooms>;
export const rooms_named: TRooms = Object.keys(new Rooms()) as TRooms;

export class Room {
  "name": string;
  "temperature": Temperature;
  "appliances": Appliance[];
  "radiator": boolean;
  "demand": Energy;

  constructor({name, temperature, appliances, radiator, demand}: IRoom) {
    this.name = name;
    this.temperature = new Temperature(temperature);
    this.appliances = [];
    this.radiator = radiator;
    this.demand = new Energy(demand);
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
  "radiator": boolean,
  "demand": number
}

export class Appliances {
  'Equipment': Appliance;
  'Lights': Appliance;
  'ElectricHeater': Appliance;
  'HeatPump': Appliance;
  'Total': Appliance;
}
export interface IAppliances extends Appliances {}
export type TAppliances = Array<keyof IAppliances>;
export const appliances_named: TAppliances = Object.keys(new Appliances()) as TAppliances;

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

export class Generators {
  'SolarPanel': Generator;
  'Windturbine': Generator;
  'SolarThermal': Generator;
  'Total': Generator;
}
export interface IGenerators extends Generators {}
export type TGenerators = Array<keyof IGenerators>
export const generators_named: TGenerators = Object.keys(new Generators()) as TGenerators

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
  "diff": Energy;

  constructor({level, stored, taken, diff}: IBattery) {
    this.level = new Energy(level);
    this.stored = new Energy(stored);
    this.taken = new Energy(taken);
    this.diff = new Energy(diff);
  }
}
export interface IBattery {
  "level": number,
  "stored": number,
  "taken": number,
  "diff": number
}

export class Grid {
  "sold": Energy;
  "bought": Energy;
  "sell": Energy;
  "buy": Energy;
  "diff": Energy;

  constructor({sold, bought, sell, buy, diff}: IGrid) {
    this.sold = new Energy(sold);
    this.bought = new Energy(bought);
    this.sell = new Energy(sell);
    this.buy = new Energy(buy);
    this.diff = new Energy(diff);
  }
}
export interface IGrid {
  "sold": number,
  "bought": number,
  "sell": number,
  "buy": number,
  "diff": number
}
