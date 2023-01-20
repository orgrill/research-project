#!/usr/bin/python3

import actions
import pandas as pd
import os
from typing import List


def load_data(folder: str, labels: List[str]) -> pd.DataFrame:
    csv_files: List[pd.DataFrame] = [pd.read_csv(f"{folder}/{f}.csv", header=None, names=[f], sep=',') for f in labels]
    return pd.concat(csv_files, axis = 1) # Use axis = 1 to concat columns (default is index)


if __name__ == '__main__':
    data_subfolder = lambda f: os.path.join(os.getcwd(), "data", f)
    station_data: pd.DataFrame = load_data(data_subfolder("CWS_StationData_Cleaned"),
                             ["datetime", "stationid", "longitude", "latitude", "elevation", "temperature"])

    projected_temps: pd.DataFrame = load_data(data_subfolder("CWS_SNAP_TMAX"),
                                              ['datetime', 'latitude', 'longitude'])

    # Add projected_temp column from projected_temps
    station_data = actions.add_projected_temps(station_data, projected_temps)

    # TODO:
    # Calculate and add bias column to station_data
    # station_data = actions.get_temp_bias(station_data)

    # TODO:
    # More stuff
