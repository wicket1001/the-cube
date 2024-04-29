
export class Energy {
  value: number = 0;

  constructor(value: number) {
    this.value = value;
  }

  public toString(): string {
    return `${this.value.toFixed()}J`;
  }

  /*
  public toString = () : string => {
    return `Bar (${this.name})`;
  }
   */

  public format_kilo_joule(): string {
    return `${(this.value / 1000).toFixed()}kJ`;
  }

  public format_watt_seconds(): string {
    return `${this.value.toFixed()}Ws`;
  }

  public format_watt_hours(): string {
    return `${(this.value / 3600).toFixed()}Wh`;
  }

  public format_kilo_watt_hours(): string {
    return `${(this.value / 3600 / 1000).toFixed()}kWh`;
  }

  public format_watt_day(): string {
    return `${(this.value / 3600 / 24).toFixed()}Wd`;
  }

  public format_kilo_watt_day(): string {
    return `${(this.value / 3600 / 1000 / 24).toFixed()}kWd`;
  }
}

export class Power {
  value: number = 0;

  constructor(value: number) {
    this.value = value;
  }

  public toString(): string {
    return `${this.value.toFixed()}W`;
  }

  public format_kilo_watt(): string {
    return `${(this.value / 1000).toFixed()}kW`;
  }
}

export class Temperature {
  value: number = 0;

  constructor(value: number) {
    this.value = value;
  }

  public toString(): string {
    return `${this.value.toFixed()}K`;
  }

  public format_celsius(): string {
    return `${(this.value - 273.15).toFixed()}°C`;
  }

  public format_fahrenheit(): string {
    return `${(this.value * (9 / 5) - 459.67).toFixed()}°F`;
  }
}

export class Money {
  value: number = 0;

  constructor(value: number) {
    this.value = value;
  }

  public toString(): string {
    return `${this.value.toFixed()}€`;
  }
}
