import type {
  IAppliance,
  IBattery,
  IGenerator,
  IGrid,
  IRoom,
  IAlgorithm,
  IEnvironment,
  IMockAlgorithm
} from '@/@types/components'
import { Appliance, Battery, Generator, Grid, Room, Algorithm, Environment, MockAlgorithm } from '@/@types/components'

export class Simulation {
  "step": number;
  "absolute_step": number;
  "environment": Environment;
  "benchmark": Algorithm;
  // "decision": Algorithm;
  "noBat": MockAlgorithm;
  "noWind": MockAlgorithm;
  "noPV": MockAlgorithm;

  constructor({step, absolute_step, environment, benchmark, noBat, noWind, noPV}: ISimulation) { /* , decision */
    this.step = step;
    this.absolute_step = absolute_step;
    this.environment = new Environment(environment);
    this.benchmark = new Algorithm(benchmark);
    // this.decision = new Algorithm(decision);
    this.noBat = new MockAlgorithm(noBat);
    this.noWind = new MockAlgorithm(noWind);
    this.noPV = new MockAlgorithm(noPV);
  }
}
export interface ISimulation {
  "step": number,
  "absolute_step": number,
  "environment": IEnvironment,
  "benchmark": IAlgorithm,
  // "decision": IAlgorithm
  "noBat": IMockAlgorithm,
  "noWind": IMockAlgorithm,
  "noPV": IMockAlgorithm,
}
