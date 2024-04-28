import csv
from datetime import datetime

from DebugLevel import DebugLevel


def read_csv(verbosity: DebugLevel):
    weather = {
        'dates': [],
        'radiations': [],
        'temperatures': [],
        'winds': [],
        'wind_directions': []
    }

    with open('res/Messstationen Zehnminutendaten v2 Datensatz_20210101T0000_20240101T0000.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        headers = reader.__next__()
        # print(headers)
        date_index = headers.index('time')
        radiation_index = headers.index('cglo')
        temperature_index = headers.index('tl')
        wind_index = headers.index('ff')
        wind_direction_index = headers.index('dd')
        if verbosity >= DebugLevel.DEBUGGING:
            print(date_index, radiation_index, temperature_index, wind_index)
        for row in reader:
            # print(len(row), ', '.join(row))
            weather['dates'].append(datetime.fromisoformat(row[date_index]))
            try:
                weather['radiations'].append(float(row[radiation_index]))
            except ValueError:
                weather['radiations'].append(0)
            weather['temperatures'].append(float(row[temperature_index]))
            weather['winds'].append(float(row[wind_index]))
            weather['wind_directions'].append(float(row[wind_direction_index]))

    if verbosity >= DebugLevel.DEBUGGING:
        print(len(weather['dates']), ', '.join([x.strftime('%d.%m.%Y %H:%M') for x in weather['dates']]))
    if verbosity >= DebugLevel.DEBUGGING:
        print(len(weather['radiations']), ', '.join([str(x) for x in weather['radiations']]))
    if verbosity >= DebugLevel.DEBUGGING:
        print(len(weather['temperatures']), ', '.join([str(x) for x in weather['outer_temperatures']]))
    if verbosity >= DebugLevel.DEBUGGING:
        print(len(weather['winds']), ', '.join([str(x) for x in weather['winds']]))

    return weather
