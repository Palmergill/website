import pandas as pd
import datetime
import utm
from geopy import distance
import numpy as np
import math

#function to convert unix time to utc time
def unix_time_to_utc(unix_time):
      return datetime.datetime.utcfromtimestamp(int(unix_time)).strftime('%Y-%m-%d %H:%M:%S.%f')

#file path to a trajectory data file, change if you want a different day
filepath = "univBuffalo_trajectory.2019_09_25_11_58_45 - univBuffalo_trajectory.2019_09_25_11_58_45.csv"

data = pd.read_csv(filepath, header = None)

# Some single times have 50+ Easting and Northing Pairs,
# This only looks at the Easting, Northing in the first column
data = data[0]


# time has length of 1500 while northing and easting are 1499,
# droping last time since it has NaN easting and Northing associated with it.
# this is to ensure all data has 3 values
timeData = data.iloc[::3]
timeData = timeData[:-1]
northingData = data.iloc[1::3]
eastingData = data.iloc[2::3]

#Had issue creating Dataframe with Series so converting to lists
timeList = timeData.tolist()
northingList = northingData.tolist()
eastingList = eastingData.tolist()


data = []
for i in range(len(timeList)):
    data.append([timeList[i],northingList[i],eastingList[i]])


#DataFrame with time matched up with Northing and Easting data in first column
GPS_df = pd.DataFrame(data, columns = ['Time', 'Northing','Easting']) 


#I got below code from holdens code, This takes the Northing and Easting Data
# Converts to lat and long

x = GPS_df['Easting']
y = GPS_df['Northing']

# The data we are working on is in UTM zone 18S, if different location is used, change variable below

zone_num = 18
zone_let = 'S'

GPS_df['Lat'] = utm.to_latlon(x, y, zone_num, zone_let)[0]
GPS_df['Long'] = utm.to_latlon(x, y, zone_num, zone_let)[1]


#convert time

GPS_df['Time'] = GPS_df['Time'].apply(unix_time_to_utc)

# output a csv file for plotting
#I was able to use these csv files on https://www.gpsvisualizer.com/

GPS_df[['Lat','Long']].to_csv("latlong.csv", index = False)

