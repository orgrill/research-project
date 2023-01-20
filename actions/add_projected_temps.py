import pandas as pd
import numpy as np
import sys
import math


def add_projected_temps(actual_data: pd.DataFrame, projected_data: pd.DataFrame) -> pd.DataFrame:
    print("<Description of what this function is going to accomplish>")

    unique_stations = actual_data[['stationid', 'latitude', 'longitude']].drop_duplicates()

    # Associate approximate lat,long in projected_data to a stationId
    for (_, projected_row) in projected_data.iterrows():
        closest_station = ""
        min_dist = sys.maxsize

        # Look for the closest stationId by computing diagonal distance between the two sets of coordinates
        #for (stationid, station_lat, station_long) in :
        for (_, unique_row) in unique_stations.iterrows():
            dist = get_distance((float(projected_row['latitude']), float(projected_row['longitude'])), 
                                (float(unique_row['latitude']), float(unique_row['longitude'])))
            if dist < min_dist:
                min_dist = dist
                closest_station = unique_row['stationid']

        # Add projected_temp column to rows with the same stationId + datetime
        actual_data.loc[(actual_data['stationid'] == closest_station) 
                        & (actual_data['datetime'] == projected_row['datetime']),
                        'projected_temp'] = projected_row['temperature']

    return actual_data


def get_distance(A: tuple, B: tuple) -> float:
    return math.sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2)

