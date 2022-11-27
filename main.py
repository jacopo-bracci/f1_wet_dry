import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROLLING_CONST = 1
AT_LEAST_MANY_RACES = 5
TIME_CORRECTION = 1.03

df_lap_times = pd.read_csv("lap_times.csv", header=0)

df_races = pd.read_csv("races.csv", header=0)[["raceId", "year", "circuitId", "name", "date"]]
df_races.set_index("raceId", inplace=True)
df_races.loc[df_races["name"] == "70th Anniversary Grand Prix", "circuitId"] = 99

"""
    INITIAL COMPUTATION
"""
# compute mean
df_raceMean = df_lap_times.groupby(["raceId"])["milliseconds"].mean()
df_raceSTD = df_lap_times.groupby(["raceId"])["milliseconds"].std()



marameo = df_raceMean.to_frame().merge(df_raceSTD, on="raceId")
marameo.rename(columns={'milliseconds_x': 'racestd', 'milliseconds_y': 'raceAverage'}, inplace=True)

print(marameo.loc[1038])


# JOIN
df_master_times = df_lap_times.merge(df_raceMean, on="raceId")
df_master_times.rename(columns={'milliseconds_x': 'raceAverage', 'milliseconds_y': 'milliseconds'}, inplace=True)

"""
    CORRECTION
"""
# CORRECT lap times -> exclude abnormal values
list_attributes = ["raceId", "milliseconds"]
df_lap_times_C = df_master_times[df_master_times['milliseconds'] < (df_master_times['raceAverage'] * TIME_CORRECTION)][list_attributes]

# TODO magia con STD

# RECOMPUTE MEAN
df_raceMean_C = df_lap_times_C.groupby(["raceId"], dropna=True)["milliseconds"].mean()
# df_raceMean_C.rename(columns={'milliseconds': 'raceAverage'}, inplace=True) # NOT A DATAFRAME



# recompute JOINED data
df_master_raceMean_C = df_races.merge(df_raceMean_C, on="raceId").sort_values(['circuitId'])# .sort_values(['name', 'year'])
df_master_raceMean_C.rename(columns={'milliseconds': 'raceAverage'}, inplace=True)

"""
    ROLLING AVERAGE
"""
# FILTER circuits that have less than AT_LEAST_MANY races
circuitsMean = df_master_raceMean_C.groupby(["circuitId"]).filter(lambda x: len(x) > AT_LEAST_MANY_RACES)

# compute ROLLING AVERAGE per circuit
circuitsMean = circuitsMean.groupby(["circuitId"])["raceAverage"]\
                                .rolling(ROLLING_CONST)\
                                .mean()\
                                .fillna(method='bfill')
circuitsMean.index.names = ['circuitId', 'raceId']

# RESETTING and setting index
circuitsMean = circuitsMean.reset_index()
circuitsMean = circuitsMean.set_index('raceId')

circuitsMean.rename(columns={'raceAverage': 'rollingCircuitAverage'}, inplace=True)



# TODO moving average on 5 past years

bigboy = df_races.merge(circuitsMean, on=["raceId"]).sort_values(['name', 'year'])
bigboy.drop(columns=["circuitId_y"], inplace=True)


bigboy['is_WET'] = False


# print(bigboy[bigboy["name"] == "Australian Grand Prix"].to_string())
print(bigboy[bigboy["name"] == "Italian Grand Prix"].to_string())

# TODO find wet-dry races










# TODO compute average over season to check eventual technical improvement -> beware wet/normal race

# print(circuitsMean.head(30).to_string())
# print(circuitsMean.info())
exit(0)