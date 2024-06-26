import axios from 'axios'
import type { Dates, GeosphereRaw } from '@/@types/geosphere'
import type { ISimulation } from '@/@types/simulation'
import { Simulation } from '@/@types/simulation'

const baseURL = `http://localhost:8080/`
const cache_size = 144;

const host = 'https://dataset.api.hub.geosphere.at'
const version = 'v1'

const start = "2021-01-20T00:00"
const end = "2021-01-21T00:00"
const parameter: string[] = ["tl", "ff", "cglo"]

const type = 'station' // ?station_ids=1,2,3
const mode = 'historical'
const resource_id = 'klima-v2-10min'

export async function getData(): Promise<{ temperatures: number[], winds: number[], radiation: number[], dates: Date[] }> {
  // https://dataset.api.hub.geosphere.at/v1/openapi-docs
  // https://dataset.api.hub.geosphere.at/v1/station/historical/klima-v1-10min?parameters=RR&start=2021-01-01T00%3A00&end=2021-01-01T00%3A00&station_ids=5882&output_format=geojson
  const url = `${host}/${version}/${type}/${mode}/${resource_id}`;
  const response = await axios.get(url, {
    params: {
      parameters: parameter,
      station_ids: 5925, // Wien Innere Stadt
      start: start,
      end: end,
      output_format: 'geojson'
    },
    paramsSerializer: {indexes: null}
    });
  const data: GeosphereRaw = response.data;
  const parameters = data['features'][0]['properties']['parameters'];
  console.log(parameters)
  const temperatures = parameters["tl"]['data']; // TODO
  const winds = parameters["ff"]['data'];
  const radiation = parameters["cglo"]['data'];
  const dates = export_dates(data)['timestamps'];
  return {temperatures: temperatures, winds: winds, radiation: radiation, dates: dates};
}

function export_dates(raw_data: GeosphereRaw): Dates {
  return { 'timestamps':
      raw_data['timestamps'].map<Date>(item => {
          return new Date(item)
        }
      )
  }
}

export async function getSimulation(): Promise<Simulation> {
  const url = `${baseURL}step`;
  const response = await axios.get(url, {
    validateStatus(status) {
        return status !== 422;
    },
  })
    .catch(function (error) {
      console.log('Nothing ever happens', error);
      return Promise.reject(error);
    });
  const data: ISimulation = response.data;
  return new Simulation(data);
}

export async function lookback_sim(absolute_step: number): Promise<Simulation[]> {
  const url = `${baseURL}step`;
  const response = await axios.get(url, {
    params: {
      lookback: Math.min(absolute_step, cache_size),
    },
    paramsSerializer: { indexes: null }
  });
  const raw_simulation: [ISimulation] = response.data;
  const simulations: Simulation[] = [];
  for (const raw of raw_simulation) {
    simulations.push(new Simulation(raw));
  }
  return simulations;
}

export async function simulate(): Promise<Simulation> {
  const url = `${baseURL}step`;
  await axios.patch(url);
  const response = await axios.get(url);
  const data: ISimulation = response.data;
  return new Simulation(data);
}

export async function patching(): Promise<boolean> {
  const url = `${baseURL}environment`;
  const response = await axios.patch(url, {
    outer_temperature: 30
  });
  return true;
}

export async function patch_future(absolute_step: number): Promise<Simulation[]> {
  const url = `${baseURL}step`;
  await axios.patch(url, {
    absolute: absolute_step
  });
  const response = await axios.get(url, {
    params: {
      lookback: Math.min(absolute_step, cache_size),
    },
    paramsSerializer: { indexes: null }
  });
  const raw_simulation: [ISimulation] = response.data;
  const simulations: Simulation[] = [];
  // return raw_simulation.map(isimulation => new Simulation(isimulation));
  for (const raw of raw_simulation) {
    simulations.push(new Simulation(raw));
  }
  return simulations;
}

export async function reset_simulation(): Promise<number> {
  const url = `${baseURL}reset`;
  const response = await axios.post(url, {});
  return response.status;
  // return response.data;
}
