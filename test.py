import pandas as pd
from typing import List
import csv


def load_cws_data(folder: str) -> pd.DataFrame:
    labels: List[str] =  ["datetime", "stationid", "longitude", "latitude", "elevation", "temperature"]


    csv_files: List[pd.DataFrame] = [pd.read_csv(f"{folder}/{f}.csv", header=None, names=[f], sep=',') for f in labels]

    # Use axis = 1 to concat columns (default is index)
    return pd.concat(csv_files, axis = 1)


def clean_cws_data(raw_cws: pd.DataFrame) -> pd.DataFrame:
    print(raw_cws)
    # Change stationid to a Categorical (Similar to an enum)
    raw_cws['stationid'] = pd.Categorical(raw_cws['stationid'])
    # Convert dates to a datetime object
    raw_cws['datetime'] = pd.to_datetime(raw_cws['datetime'], format = "%Y-%m-%d")
    # Drop rows that have NaN temperatures
    #raw_cws = raw_cws.dropna(subset = ['temperature'])
    
    return raw_cws


def load_training_data() -> pd.DataFrame:
    data = pd.read_csv("trainingdata.csv", header = None, names = ['bias', 'elevation', 'day'])
    return data


def clean_training_data(data: pd.DataFrame):
    pass


def plot_training_data():
    data: pd.DataFrame = clean_training_data(load_training_data())

#def load_SNAPdata() -> pd.DataFrame:
    #data = pd.read_csv("SNAP_Lat.csv", header = None)
    #return data

#def load_SNAPdata() -> pd.DataFrame:
    #data = pd.read_csv("SNAP_Long.csv", header = None)
    #return data


if __name__ == '__main__':
    cws: pd.DataFrame = clean_cws_data(load_cws_data("CWS_StationData"))
    cws_cleaned: pd.DataFrame = clean_cws_data(load_cws_data("CWS_StationData_Cleaned"))


    filtered_cws = cws.loc[(cws['stationid'] == 'RAWS_CHITITU')]
                            #& (cws['temperature']  > 5) 
                           # & (cws['temperature'] < 20)]
                        
    filtered_cws_cleaned = cws.loc[(cws['stationid'] == 'USC00509139')]
                            #& (cws['temperature']  > 5) 
                           # & (cws['temperature'] < 20)]

    print(filtered_cws_cleaned['temperature'].describe())
    filtered_cws.plot.scatter(x='datetime', y = 'temperature')
    
    
    ##This gives details about the data, cws and cws_cleaned

#print(cws['stationid'].value_counts())
#print(cws_cleaned['stationid'].value_counts())

print(cws_cleaned['stationid'].describe())
print(cws['stationid'].describe())

#Stats for individual station id's just change quotes after ==
print(cws_cleaned.loc[cws_cleaned["stationid"] == 'RAWS_CHITITU'].describe())


actualData : pd.DataFrame = ("CWS_StationData_Cleaned\stationdata_coordinates.csv")
projectedData : pd.DataFrame = ("CWS_SNAP_TMAX\coordinates.csv") 
projectedData_fixed : pd.DataFrame = ()

#Pick random weather station
#manually calculate bias for weather station and compare it to training data col 1

actualData : pd.DataFrame = ("CWS_StationData_Cleaned\stationdata_coordinates.csv")
projectedData : pd.DataFrame = ("CWS_SNAP_TMAX\coordinates.csv") 
projectedData_fixed : pd.DataFrame = ()

# associate stationIds to actual coordinates
# create a python dictionary where the keys are stationids and the values are lat,long

##Not sure how to make sure that the station id matches the right lat long coordinates##

station_coordinates = {station: actualData.loc[actualData['stationid'] == station].coordinates for station in actualData['stationid'].unique}

for projectedRow in projectedData:
    # calculate distance to every unique station

    closestStation = "" # put the stationID of the closest station here
    for station, coordinates in station_coordinates:
        # calculate distance between projectedRow.coordinates and coordinates
        # take the lowest distance and it's associated stationid
        #closestStation = result

    projectedData_fixed.add_row(closestStation, projectedRow.temperatures)

# compare

for row in projectedData_fixed:
    if (row.temperatures == actualData.loc[actualData['stationid'] == row['stationid']]):
        # do something
       
      
import pandas as pd

#Merging latitude and longitude into coordinate pairs for GCM data
# Read in the latitude CSV file
lat_df = pd.read_csv("CWS_SNAP_TMAX\SNAP_Lat.csv")

# Read in the longitude CSV file
lon_df = pd.read_csv("CWS_SNAP_TMAX\SNAP_Long.csv")

# Make sure the files have the same shape (21x24 matrix, not in traditional columns/rows format)
if lat_df.shape != lon_df.shape:
    raise ValueError("The files don't have the same shape.")

# Create a new dataframe with latitude and longitude columns
merged_df = pd.DataFrame(columns=['latitude', 'longitude'])
merged_df['latitude'] = lat_df.values.flatten()
merged_df['longitude'] = lon_df.values.flatten()

# Write the merged dataframe to a new CSV file

#Uncomment to write csv
# merged_df.to_csv("coordinates.csv", index=False)

########################################################################################################################################

#Same as above but for station data including stationid
stationid_df = pd.read_csv("CWS_StationData_Cleaned\stationid.csv")
lat_df = pd.read_csv("CWS_StationData_Cleaned\latitude.csv")
lon_df = pd.read_csv("CWS_StationData_Cleaned\longitude.csv")

# Make sure the files have the same number of rows
if len(lat_df) != len(lon_df) or len(lat_df) != len(stationid_df):
    raise ValueError("The files don't have the same number of rows.")

# Create a new dataframe with stationid, latitude and longitude columns
merged_df = pd.DataFrame(columns=['stationid','latitude', 'longitude'])
merged_df["stationid"] = stationid_df.iloc[:,0]
merged_df['latitude'] = lat_df.iloc[:,0]
merged_df['longitude'] = lon_df.iloc[:,0]

# Write the merged dataframe to a new CSV file

# Uncomment to write csv
#merged_df.to_csv("stationdata_coordinates.csv", index=False) 
