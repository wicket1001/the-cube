import axios from 'axios'
import type { Dates, GeosphereRaw } from '@/@types/geosphere'

const host = 'https://dataset.api.hub.geosphere.at'
const version = 'v1'

const start = "2021-01-20T00:00"
const end = "2021-01-21T00:00"
const parameter: string[] = ["tl", "ff", "cglo"]

const type = 'station' // ?station_ids=1,2,3
const mode = 'historical'
const resource_id = 'klima-v2-10min'

export async function getData(): Promise<{ temperatures: number[], winds: number[], radiation: number[], dates: Date[] }> {
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