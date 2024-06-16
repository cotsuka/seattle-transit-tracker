""" Seattle Train Tracker main loop """
import time
from .data import Seattle
from .model import (
    Agency,
    LED,
    Route,
    Stop
)

START_TIME = time.monotonic()
SEATTLE = Seattle()

# routes and stops won't change often, so simply hardcode
link1_stops = {
    '40_1108': Stop('40_1108', 'Westlake', 'SW', LED(0)),
    '40_1121': Stop('40_1121', 'Westlake', 'NE', LED(0)),
    '40_455': Stop('40_455', 'University St', 'SE', LED(0)),
    '40_501': Stop('40_501', 'Pioneer Square', 'SE', LED(0)),
    '40_532': Stop('40_532', 'Pioneer Square', 'NW', LED(0)),
    '40_55578': Stop('40_55578', 'Rainier Beach', 'N', LED(0)),
    '40_55656': Stop('40_55656', 'Othello', 'NW', LED(0)),
    '40_55778': Stop('40_55778', 'Columbia City', 'NW', LED(0)),
    '40_55860': Stop('40_55860', 'Mount Baker', 'NW', LED(0)),
    '40_55949': Stop('40_55949', 'Mount Baker', 'SE', LED(0)),
    '40_56039': Stop('40_56039', 'Columbia City', '', LED(0)),
    '40_56159': Stop('40_56159', 'Othello', 'SE', LED(0)),
    '40_56173': Stop('40_56173', 'Rainier Beach', 'S', LED(0)),
    '40_565': Stop('40_565', 'University St', 'NW', LED(0)),
    '40_621': Stop('40_621', "Int'l Dist/Chinatown", 'N', LED(0)),
    '40_623': Stop('40_623', "Int'l Dist/Chinatown", 'S', LED(0)),
    '40_990001': Stop('40_990001', 'U District', 'S', LED(0)),
    '40_990002': Stop('40_990002', 'U District', 'N', LED(0)),
    '40_990003': Stop('40_990003', 'Roosevelt', 'S', LED(0)),
    '40_990004': Stop('40_990004', 'Roosevelt', 'N', LED(0)),
    '40_990005': Stop('40_990005', 'Northgate', '', LED(0)),
    '40_990006': Stop('40_990006', 'Northgate', '', LED(0)),
    '40_99101': Stop('40_99101', 'Stadium', 'S', LED(0)),
    '40_99111': Stop('40_99111', 'SODO', '', LED(0)),
    '40_99121': Stop('40_99121', 'Beacon Hill', 'E', LED(0)),
    '40_99240': Stop('40_99240', 'Beacon Hill', 'W', LED(0)),
    '40_99256': Stop('40_99256', 'SODO', 'N', LED(0)),
    '40_99260': Stop('40_99260', 'Stadium', 'N', LED(0)),
    '40_99603': Stop('40_99603', 'Capitol Hill', '', LED(0)),
    '40_99604': Stop('40_99604', 'Univ of Washington', 'S', LED(0)),
    '40_99605': Stop('40_99605', 'Univ of Washington', 'N', LED(0)),
    '40_99610': Stop('40_99610', 'Capitol Hill', 'S', LED(0)),
    '40_99900': Stop('40_99900', "Tukwila Int'l Blvd", 'W', LED(0)),
    '40_99903': Stop('40_99903', "SeaTac/Airport", '', LED(0)),
    '40_99904': Stop('40_99904', "SeaTac/Airport", '', LED(0)),
    '40_99905': Stop('40_99905', "Tukwila Int'l Blvd", 'E', LED(0)),
    '40_99913': Stop('40_99913', 'Angle Lake', '', LED(0)),
    '40_99914': Stop('40_99914', 'Angle Lake', '', LED(0))
}
Link1Line = Route('40_100479', 'Link 1 Line')
Link1Line.stops = link1_stops

link2_stops = {
    '40_E09-T2': Stop('40_E09-T2', 'South Bellevue', '', LED(0)),
    '40_E11-T1': Stop('40_E11-T1', 'East Main', 'S', LED(0)),
    '40_E11-T2': Stop('40_E11-T2', 'East Main', 'N', LED(0)),
    '40_E15-T1': Stop('40_E15-T1', 'Bellevue Downtown', 'W', LED(0)),
    '40_E15-T2': Stop('40_E15-T2', 'Bellevue Downtown', 'E', LED(0)),
    '40_E19-T1': Stop('40_E19-T1', 'Wilburton', 'S', LED(0)),
    '40_E19-T2': Stop('40_E19-T2', 'Wilburton', 'N', LED(0)),
    '40_E21-T1': Stop('40_E21-T1', 'Spring District', 'W', LED(0)),
    '40_E21-T2': Stop('40_E21-T2', 'Spring District', 'E', LED(0)),
    '40_E23-T1': Stop('40_E23-T1', 'BelRed', 'W', LED(0)),
    '40_E23-T2': Stop('40_E23-T2', 'BelRed', 'E', LED(0)),
    '40_E25-T1': Stop('40_E25-T1', 'Overlake Village', 'SW', LED(0)),
    '40_E25-T2': Stop('40_E25-T2', 'Overlake Village', 'NE', LED(0)),
    '40_E27-T1': Stop('40_E27-T1', 'Redmond Technology', '', LED(0)),
    '40_E27-T2': Stop('40_E27-T2', 'Redmond Technology', '', LED(0))
}
Link2Line = Route('40_2LINE', 'Link 2 Line')
Link2Line.stops = link2_stops

SoundTransit = Agency(40, 'Sound Transit')
SoundTransit.routes = {
    '40_100479': Link1Line,
    '40_2LINE': Link2Line
}

while True:
    for route in SoundTransit.routes.keys():
        trips = SEATTLE.get_trips(route)
        stop_ids: list[str] = []
        for trip in trips:
            closest_stop_id = trip['status']['closestStop']
            stop_ids.append(closest_stop_id)
        for stop_id, stop in SoundTransit.routes[route].stops.items():
            if stop_id in stop_ids:
                stop.led.color = (255, 255, 255)
            else:
                stop.led.color = (0, 0, 0)

    # TODO: address LEDs instead of printing
    for route in SoundTransit.routes.values():
        for key, value in route.stops.items():
            print(key, ': ', value.led.color)
    print('\n')
    time.sleep(60.0 - ((time.monotonic() - START_TIME) % 60.0))