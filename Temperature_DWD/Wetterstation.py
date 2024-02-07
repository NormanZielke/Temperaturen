import math as m
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
plt.style.use("seaborn-v0_8")

# load downloaded rawdata from DWD --> source: https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/

Wetterstationen=["Berlin_Kaniswall","Berlin_Marzahn","Heckelberg","Münchberg"]

Berlin_Kaniswall_raw_amb = pd.read_csv(r"Temperatures_rawdata\Berlin-Kaniswall_Temp_amb\produkt_tu_stunde_20040501_20200615_00410.txt",
                 index_col = 1, sep=";")
Berlin_Kaniswall_raw_soil = pd.read_csv(r"Temperatures_rawdata\Berlin-Kaniswall_Temp_soil\produkt_eb_stunde_19960601_20181210_00410.txt",
                 index_col = 1, sep=";")
Berlin_Marzahn_raw_amb = pd.read_csv(r"Temperatures_rawdata\Berlin_Marzahn_Temp_amb\produkt_tu_stunde_20070801_20221231_00420.txt",
                 index_col = 1, sep=";")
Berlin_Marzahn_raw_soil = pd.read_csv(r"Temperatures_rawdata\Berlin_Marzahn_Temp_soil\produkt_eb_stunde_19930501_20221231_00420.txt",
                 index_col = 1, sep=";")
Heckelberg_raw_amb = pd.read_csv(r"Temperatures_rawdata\Heckelberg_Temp_amb\produkt_tu_stunde_20061201_20221231_07389.txt",
                 index_col = 1, sep=";")
Heckelberg_raw_soil = pd.read_csv(r"Temperatures_rawdata\Heckelberg_Temp_soil\produkt_eb_stunde_20061201_20221231_07389.txt",
                 index_col = 1, sep=";")
Müncheberg_raw_amb = pd.read_csv(r"Temperatures_rawdata\Müncheberg_Temp_amb\produkt_tu_stunde_19910101_20221231_03376.txt",
                 index_col = 1, sep=";")
Müncheberg_raw_soil = pd.read_csv(r"Temperatures_rawdata\Müncheberg_Temp_soil\produkt_eb_stunde_19730101_20221231_03376.txt",
                 index_col = 1, sep=";")

# --------------------------------------------------------------------------------------------------------------------->
# create DateTime-Index mit hourly frequency for year
global date_range
start_date = "2011-01-01 00:00:00"
end_date = "2011-12-31 23:00:00"
date_range = pd.date_range(start=start_date, end=end_date, freq='H')

    # function to collect dataframe from raw-data
    # year = 2011
    # input values
        #df_raw_amb = raw data for air temperature
        #df.raw_soil = raw data for ground temperature --> t_soil at a depth of 100 cm
    # output
        #df of the weatherstation with timeseries of t_amb and t_soil
def df_temperatures_2011(df_raw_amb,df_raw_soil):
    # extract timeseries for 2011
    df_amb = df_raw_amb.loc[2011010100:2011123123, :]
    df_soil = df_raw_soil.loc[2011010100:2011123123, :]
    data = {"temp_amb": df_amb.loc[:, "TT_TU"].values,
            "temp_soil": df_soil.loc[:, 'V_TE100'].values #"V_TE100" = Temperature in the soil at a depth of 100 cm
            }
    temperatures_2011 = pd.DataFrame(data,index=date_range)
    #filename_with_station = f"{'temperatures_2011'}_{station}.csv"
    #temperatures_2011.to_csv(filename_with_station,index=False)
    return temperatures_2011

df_Berlin_Kaniswall = df_temperatures_2011(Berlin_Kaniswall_raw_amb,Berlin_Kaniswall_raw_soil)
df_Berlin_Marzahn = df_temperatures_2011(Berlin_Marzahn_raw_amb,Berlin_Marzahn_raw_soil)
df_Müncheberg = df_temperatures_2011(Müncheberg_raw_amb,Müncheberg_raw_soil)

# --------------------------------------------------------------------------------------------------------------------->
# ----> in Heckelberg there are missing values for t_amb & t_soil
    # missing values in t_soil (see metadata -> "V_TE100") will be placed by linear approximation
    # to replace missing values in t_amb, we use weather station Zehdenick

Zehdenick_raw_amb = pd.read_csv(r"Temperatures_rawdata\Zehdenick_Temp_amb\produkt_tu_stunde_19810101_20221231_05745.txt",
                 index_col = 1, sep=";")

Zehdenick_raw_soil = pd.read_csv(r"Temperatures_rawdata\Zehdenick_Temp_soil\produkt_eb_stunde_19560101_20221231_05745.txt",
                 index_col = 1, sep=";")

df_Zehdenick = df_temperatures_2011(Zehdenick_raw_amb,Zehdenick_raw_soil)

# create empty dataframe for Heckelberg
data = {"temp_amb": {},
        "temp_soil": {}
}
df_Heckelberg = pd.DataFrame(data,index=date_range)

# fill dataframe with known values
df_Heckelberg.loc["2011-01-01 00:00:00":"2011-04-26 16:00:00","temp_soil"] = Heckelberg_raw_soil.loc[2011010100:2011042616,'V_TE100'].values
df_Heckelberg.loc["2011-04-28 10:00:00":"2011-06-29 06:00:00","temp_soil"] = Heckelberg_raw_soil.loc[2011042810:2011062906,'V_TE100'].values
df_Heckelberg.loc["2011-06-29 09:00:00":"2011-07-01 12:00:00","temp_soil"] = Heckelberg_raw_soil.loc[2011062909:2011070112,'V_TE100'].values
df_Heckelberg.loc["2011-07-01 16:00:00":"2011-12-31 23:00:00","temp_soil"] = Heckelberg_raw_soil.loc[2011070116:2011123123,'V_TE100'].values
df_Heckelberg.loc["2011-01-01 00:00:00":"2011-04-26 16:00:00","temp_amb"] = Heckelberg_raw_amb.loc[2011010100:2011042616,'TT_TU'].values
df_Heckelberg.loc["2011-04-28 10:00:00":"2011-07-01 12:00:00","temp_amb"] = Heckelberg_raw_amb.loc[2011042810:2011070112,'TT_TU'].values
df_Heckelberg.loc["2011-07-01 16:00:00":"2011-12-31 23:00:00","temp_amb"] = Heckelberg_raw_amb.loc[2011070116:2011123123,'TT_TU'].values
# missing values in t_soil (see metadata -> "V_TE100") will be placed by linear approximation

missing_starts = ["2011-04-26 17:00:00","2011-06-29 07:00:00","2011-07-01 13:00:00"]
missing_ends = ["2011-04-28 09:00:00","2011-06-29 08:00:00","2011-07-01 15:00:00"]


    # function to approximate missing values
    # input values
        # df
        # starting point of missing intervall
        # end point of missing intervall
    # output
        # df of the weatherstation with timeseries of t_amb and t_soil
def approximate(df,missing_start_date,missing_end_date):
    missing_range = pd.date_range(start=missing_start_date, end=missing_end_date, freq='H')
    t_delta = (df.loc[df.index[df.index > pd.to_datetime(missing_end_date)].min(),"temp_soil"] -
               df.loc[df.index[df.index < pd.to_datetime(missing_start_date)].max(),"temp_soil"])
    if t_delta == 0:
        missing_values = np.full(len(missing_range),df.loc[df.index[df.index > pd.to_datetime(missing_end_date)].min(),"temp_soil"])
    else:
        x = t_delta/len(missing_range)
        missing_values = np.arange(df.loc[df.index[df.index < pd.to_datetime(missing_start_date)].max(),"temp_soil"],
                                   df.loc[df.index[df.index > pd.to_datetime(missing_end_date)].min(),"temp_soil"],x)
    df.loc[missing_start_date:missing_end_date,"temp_soil"] = missing_values
    return

for missing_start_date,missing_end_date in zip(missing_starts,missing_ends):
    approximate(df_Heckelberg,missing_start_date,missing_end_date)

# ----> fill missing values of temp_amb
    # plot timeseries through timeintervall of missing of Heckelberg and Zehdenick
    # to evaluate if we can replace the missing data with the data given by Zehdenick
def plotten(df,color,axes):
    df.plot(ax=axes,color=color,linewidth=1, alpha=1)
    axes.set_ylabel("[°C]", fontsize=12, family="monospace", rotation="horizontal")
    axes.yaxis.set_label_coords(-0.060, 0.920)

fig, axes = plt.subplots(2, 1, figsize=(12, 8))
plotten(df_Heckelberg.loc["2011-04-25 00:00:00":"2011-05-02 00:00:00", "temp_amb"], "darkblue", axes[0])
plotten(df_Zehdenick.loc["2011-04-25 00:00:00":"2011-05-02 00:00:00", "temp_amb"], "goldenrod", axes[0])

plotten(df_Heckelberg.loc["2011-06-28 00:00:00":"2011-07-03 00:00:00", "temp_amb"], "darkblue", axes[1])
plotten(df_Zehdenick.loc["2011-06-28 00:00:00":"2011-07-03 00:00:00", "temp_amb"], "goldenrod", axes[1])

axes[0].legend(["t_amb - H", "t_amb - Z"],prop={"family": "serif"})
axes[1].legend(["t_amb - H", "t_amb - Z"],prop={"family": "serif"})
plt.tight_layout()
plt.show()

df_Heckelberg.loc["2011-04-26 17:00:00":"2011-04-28 09:00:00","temp_amb"] = df_Zehdenick.loc["2011-04-26 17:00:00":"2011-04-28 09:00:00","temp_amb"]
df_Heckelberg.loc["2011-07-01 13:00:00":"2011-07-01 15:00:00","temp_amb"] = df_Zehdenick.loc["2011-07-01 13:00:00":"2011-07-01 15:00:00","temp_amb"]
# Test if columns are full
# df_Heckelberg.loc[:,"temp_amb"].isna().unique()
# df_Heckelberg.loc[:,"temp_soil"].isna().unique()
# --------------------------------------------------------------------------------------------------------------------->
# ----> collect Data for Communities from weather stations

Gemeinden = ["Rüdersdorf bei Berlin","Strausberg","Erkner","Grünheide (Mark)"]
ags_id = [12064428,12064472,12067124,12067201]

# Rüdersorf bei Berlin -> Berlin-Marzahn/Müncheberg arithmetic mean
df_Rüdersdorf = (df_Berlin_Marzahn + df_Müncheberg)/2
df_Rüdersdorf.insert(0,"ags_id",np.full(len(date_range),12064428))

# Strausberg -> Berlin-Kaniswall/Berlin-Marzahn/Heckelber/Müncheberg arithmetic mean
df_Strausberg = (df_Berlin_Kaniswall + df_Berlin_Marzahn + df_Heckelberg + df_Müncheberg)/4
df_Strausberg.insert(0,"ags_id",np.full(len(date_range),12064472))

# Erkner -> Berlin-Kaniswall
data = {"temp_amb": {},
        "temp_soil": {}
}
df_Erkner = pd.DataFrame(data,index=date_range)
df_Erkner.loc[:,["temp_amb", "temp_soil"]] = df_Berlin_Kaniswall.loc[:,["temp_amb", "temp_soil"]]
df_Erkner.insert(0,"ags_id", np.full(len(date_range),12067124))

# Grünheide (Mark) -> Berlin-Kaniswall/Müncheberg arithmetic mean
df_Grünheide_Mark = (df_Berlin_Kaniswall + df_Müncheberg)/2
df_Grünheide_Mark.insert(0,"ags_id",np.full(len(date_range),12067201))

df = pd.concat([df_Rüdersdorf,df_Strausberg,df_Erkner,df_Grünheide_Mark])
df.sort_index(inplace=True)

data = dict(timestamp=df.index,
            ags_id=df.loc[:, "ags_id"].values,
            temp_amb=df.loc[:, "temp_amb"].values.round(2),
            temp_soil=df.loc[:, "temp_soil"].values.round(2))
temperatures_2011 = pd.DataFrame(data)

temperatures_2011.to_csv("temperatures_2011",index=False)

# --------------------------------------------------------------------------------------------------------------------->
# all cities are located in different federal states (Bundesländern)
    # create script, which deliver DataFrame contains values about weatherstations closest to a certain geo point

# load Dataframe with all waetherstations, which deliver values for t_amb
    # source: https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/air_temperature/historical/
weatherstations_t_amb = pd.read_csv(r"Wetterstationen\TU_Stundenwerte_Beschreibung_Stationen_t_amb.csv",
                                    encoding='latin1', sep=";")
# geo data cities
position_cities = {
    "Ingolstadt": {"lon": 11.4237, "lat": 48.766},  # IN
    "Kassel": {"lon": 9.479, "lat": 51.312},        # KS
    "Bocholt": {"lon": 6.614, "lat": 51.838},       # BOH
    "Kiel": {"lon": 10.123, "lat": 54.322},         # KI
    "Zwickau": {"lon": 12.461, "lat": 50.706},      # Z
}
    # function to calculate distance between two geo point with Haversine formula
        # input values
            # lon1,lat1,lon2,lat2
        # output
            # distance in [km]
def haversine(lon1,lat1,lon2,lat2):
    R = 6371.0  # radius of the earth km

    # Conversion of latitude and longitude from degrees to radians
    lat1 = m.radians(lat1)
    lon1 = m.radians(lon1)
    lat2 = m.radians(lat2)
    lon2 = m.radians(lon2)

    # Calculate deltas
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = m.sin(dlat / 2)**2 + m.cos(lat1) * m.cos(lat2) * m.sin(dlon / 2)**2
    c = 2 * m.atan2(m.sqrt(a), m.sqrt(1 - a))
    distance = R * c

    return distance
    # function which sorts a DataFrame "weatherstations" to deliver the weatherstations closest to a geo point
        # input values
            # lon1,lat1,lon2,lat2
        # output
            # distance in [km]
def closestweatherstations(lat,lon):
    distance_array = []
    lon1 = lon
    lat1 = lat

    for station in weatherstations_t_amb["Stations_id"].values:
        distance = haversine(lon1, lat1,
                             weatherstations_t_amb.loc[weatherstations_t_amb.loc[weatherstations_t_amb.Stations_id == station].index, "lon"],
                             weatherstations_t_amb.loc[weatherstations_t_amb.loc[weatherstations_t_amb.Stations_id == station].index, "lat"])
        distance_array.append(round(distance, 2))

    data = {"Distance": distance_array,
            "Stations_id": weatherstations_t_amb.loc[:, "Stations_id"].values,
            "Stationsname": weatherstations_t_amb.loc[:, "Stationsname"].values,
            "lat": weatherstations_t_amb.loc[:, "lat"].values,
            "lon": weatherstations_t_amb.loc[:, "lon"].values
            }
    df_distance = pd.DataFrame(data,index=weatherstations_t_amb.index.values)
    df_distance.sort_values(by='Distance', inplace=True)
    df_distance.reset_index(drop=True, inplace=True)

    return df_distance

# --------------------------------------------------------------------------------------------------------------------->
weatherstations_IN = closestweatherstations(position_cities["Ingolstadt"]["lat"],position_cities["Ingolstadt"]["lon"])

print("Closest weather stations for t_amb near Ingolstadt")
print(weatherstations_IN.head(5))
# closest weatherstation is "Kösching"
    # -> missing data in t_amb 13.02.2011-11:00	-> 14.02.2011-00:00	[14]
    # to replace missing values we choose we choose "Neuburg"
        # Ingolstadt-Manching -> missing values in same time
        # Karlshuld -> not in operation anymore
        # Königsmoos-Untermaxfeld -> not in operation anymore
    # -> missing values in t_soil 13.02.2011-09:00 -> 14.02.2011-07:00 [23]

Kösching_raw_amb = pd.read_csv(r"Temperatures_rawdata\Städte\Kösching_Temp_amb\produkt_tu_stunde_20041201_20221231_02700.txt",
                               index_col = 1, sep=";")
Kösching_raw_soil = pd.read_csv(r"Temperatures_rawdata\Städte\Kösching_Temp_soil\produkt_eb_stunde_19870101_20221231_02700.txt",
                                index_col = 1, sep=";")
Neuburg_raw_amb = pd.read_csv(r"Temperatures_rawdata\Städte\Neuburg_Temp_amb\produkt_tu_stunde_20020101_20221231_03484.txt",
                              index_col = 1, sep=";")
Gelbelsee_raw_amb = pd.read_csv(r"Temperatures_rawdata\Städte\Gelbelsee_Temp_amb\produkt_tu_stunde_19910101_20221231_01587.txt",
                              index_col = 1, sep=";")


# create empty dataframe for Kösching
data = {"temp_amb": {},
        "temp_soil": {}
}
df_Kösching = pd.DataFrame(data, index=date_range)
df_Neuburg = pd.DataFrame(data, index=date_range) # also missing values in Neuburg_raw_amb -> df_temperatures_2011(df_raw_amb,df_raw_soil) not running
df_Gelbelsee = pd.DataFrame(data, index=date_range)

# fill dataframe with known values
df_Kösching.loc["2011-01-01 00:00:00":"2011-02-13 10:00:00", "temp_amb"] = Kösching_raw_amb.loc[2011010100:2011021310, 'TT_TU'].values
df_Kösching.loc["2011-02-14 01:00:00":"2011-12-31 23:00:00", "temp_amb"] = Kösching_raw_amb.loc[2011021401:2011123123, 'TT_TU'].values
df_Kösching.loc["2011-01-01 00:00:00":"2011-02-13 08:00:00", "temp_soil"] = Kösching_raw_soil.loc[2011010100:2011021308, 'V_TE100'].values
df_Kösching.loc["2011-02-14 08:00:00":"2011-12-31 23:00:00", "temp_soil"] = Kösching_raw_soil.loc[2011021408:2011123123, 'V_TE100'].values
# fill dataframe with data around the missing interval of t_amb for plotting
df_Neuburg.loc["2011-02-12 05:00:00":"2011-02-15 07:00:00", "temp_amb"] = Neuburg_raw_amb.loc[2011021205:2011021507, 'TT_TU'].values
df_Gelbelsee.loc["2011-02-12 05:00:00":"2011-02-15 07:00:00", "temp_amb"] = Gelbelsee_raw_amb.loc[2011021205:2011021507, 'TT_TU'].values

df_inter = (df_Neuburg + df_Gelbelsee)/2


fig, axes = plt.subplots(1, 1, figsize=(12, 8))
plotten(df_Kösching.loc["2011-02-12 05:00:00":"2011-02-15 07:00:00", "temp_amb"], "darkblue", axes)
plotten(df_Neuburg.loc["2011-02-12 05:00:00":"2011-02-15 07:00:00", "temp_amb"], "goldenrod", axes)
plotten(df_Gelbelsee.loc["2011-02-12 05:00:00":"2011-02-15 07:00:00", "temp_amb"], "forestgreen", axes)
plotten(df_inter.loc["2011-02-12 05:00:00":"2011-02-15 07:00:00", "temp_amb"], "black", axes)

axes.legend(["t_amb - Kösching", "t_amb - Neuburg", "t_amb - Gelbelsee"],
            prop={"family": "serif"})
plt.tight_layout()
plt.show()

fig, axes = plt.subplots(1, 1, figsize=(12, 8))
plotten(df_Kösching.loc["2011-01-01 00:00:00":"2011-12-31 23:00:00", "temp_amb"], "darkblue", axes)
plotten(df_Neuburg.loc["2011-01-01 00:00:00":"2011-12-31 23:00:00", "temp_amb"], "goldenrod", axes)
plotten(df_Gelbelsee.loc["2011-01-01 00:00:00":"2011-12-31 23:00:00", "temp_amb"], "forestgreen", axes)
plotten(df_inter.loc["2011-01-01 00:00:00":"2011-12-31 23:00:00", "temp_amb"], "black", axes)

axes.legend(["t_amb - Kösching", "t_amb - Neuburg", "t_amb - Gelbelsee", "t_amb - Neuburg/Gelbelsee (mean)"],
            prop={"family": "serif"})
plt.tight_layout()
plt.show()

#closest_Kösching = closestweatherstations(11.4872,48.8302)