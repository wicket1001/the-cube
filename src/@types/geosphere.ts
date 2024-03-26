export interface GeosphereRaw {
  "media_type": string,
  "type": string,
  "version": string,
  "timestamps": string[],
  "features": [
    {
      "type": string,
      "geometry": {
        "type": string,
        "coordinates": number[]
      },
      "properties": {
        "parameters": {
          "rr": {
            "name": string,
            "unit": string,
            "data": number[]
          },
          "tl": {
            "name": string,
            "unit": string,
            "data": number[]
          }
        }
      },
      "station": string
    }
  ]
}

export interface Dates {
  "timestamps": Date[]
}

export interface Geosphere {
  "media_type": string,
  "type": string,
  "version": string,
  "timestamps": Date[],
  "features": [
    {
      "type": string,
      "geometry": {
        "type": string,
        "coordinates": number[]
      },
      "properties": {
        "parameters": {
          "RR": {
            "name": string,
            "unit": string,
            "data": number[]
          }
        }
      },
      "station": string
    }
  ]
}