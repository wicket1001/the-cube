import type { IAppliance, IBattery, IGenerator, IGrid, IRoom, IAlgorithm, IEnvironment } from '@/@types/components'
import { Appliance, Battery, Generator, Grid, Room, Algorithm, Environment } from '@/@types/components'

export class Simulation {
  "step": number;
  "absolute_step": number;
  "environment": Environment;
  "benchmark": Algorithm;
  "decision": Algorithm;

  constructor({step, absolute_step, environment, benchmark, decision}: ISimulation) {
    this.step = step;
    this.absolute_step = absolute_step;
    this.environment = new Environment(environment);
    this.benchmark = new Algorithm(benchmark);
    this.decision = new Algorithm(decision);
  }
}
export interface ISimulation {
  "step": number,
  "absolute_step": number,
  "environment": IEnvironment,
  "benchmark": IAlgorithm
  "decision": IAlgorithm
}
