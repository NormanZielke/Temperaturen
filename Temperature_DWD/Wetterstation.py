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
    # missing intervals
        # temp_amb:     26.04.2011-17:00 -> 28.04.2011-09:00 [41]
#                       01.07.2011-13:00 -> 01.07.2011-15:00 [3]
        # temp_soil:    26.04.2011-17:00 -> 28.04.2011-09:00 [41]
#                       29.06.2011-07:00 -> 29.06.2011-08:00 [2]
#                       01.07.2011-13:00 -> 01.07.2011-15:00 [3]
    # missing values in t_soil will be placed by linear approximation
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

    # function to approximate missing values in temp_soil
        # if the missing interval is greater than or near 2 days (48 values), maybe you have to check if there are peaks
    # input values
        # df -> Dataframe with column named "temp_soil"
        # starting point of missing intervall
        # end point of missing intervall
    # output
        # missing intervals of df are be filled by linear approximation
def approximate(df,missing_start_date,missing_end_date):
    missing_range = pd.date_range(start=missing_start_date, end=missing_end_date, freq='H')
    t_delta = (df.loc[df.index[df.index > pd.to_datetime(missing_end_date)].min(),"temp_soil"] -
               df.loc[df.index[df.index < pd.to_datetime(missing_start_date)].max(),"temp_soil"])
    if t_delta == 0:
        missing_values = np.full(len(missing_range),
                                 df.loc[df.index[df.index > pd.to_datetime(missing_end_date)].min(),"temp_soil"])
    else:
        missing_values = np.linspace(df.loc[df.index[df.index < pd.to_datetime(missing_start_date)].max(), "temp_soil"],
                                     df.loc[df.index[df.index > pd.to_datetime(missing_end_date)].min(), "temp_soil"],
                                     len(missing_range), endpoint=False)
    df.loc[missing_start_date:missing_end_date,"temp_soil"] = missing_values
    return

missing_starts = ["2011-04-26 17:00:00","2011-06-29 07:00:00","2011-07-01 13:00:00"]
missing_ends = ["2011-04-28 09:00:00","2011-06-29 08:00:00","2011-07-01 15:00:00"]

for missing_start_date,missing_end_date in zip(missing_starts,missing_ends):
    approximate(df_Heckelberg,missing_start_date,missing_end_date)

# check approximation for 26.04.2011-17:00 -> 28.04.2011-09:00 [41]
    # plot around missing interval -> +- 1 week
fig, axes = plt.subplots(1, 1, figsize=(8, 6))

df_Heckelberg.loc["18.04.2011-17:00":"05.05.2011-09:00", "temp_soil"].plot(ax=axes, color="darkblue", linewidth=1, alpha=1)
df_Zehdenick.loc["18.04.2011-17:00":"05.05.2011-09:00", "temp_soil"].plot(ax=axes, color="goldenrod", linewidth=1, alpha=1)
#labeling
axes.set_title("check approximation for Heckelberg in temp_soil \n with closest weatherstation Zedehnick",
               fontsize = 12,family="serif")
axes.set_ylabel("[°C]", fontsize=10, family="monospace", rotation="horizontal")
axes.yaxis.set_label_coords(-0.025, 0.980)
axes.legend(["Heckelberg", "Zehdenick"], prop={"family": "serif"})
plt.tight_layout()
plt.savefig("plots/Heckelberg_check_approx.jpg", format="jpg")

# ----> fill missing values of temp_amb
    # plot timeseries through timeintervalls of missing values of Heckelberg
    # to evaluate if we can replace the missing data with the data given by Zehdenick

fig, axes = plt.subplots(2, 1, figsize=(12, 8))
fig.suptitle("compare t_amb Heckelberg and Zehdenick",fontsize = 12,family="serif")
df_Heckelberg.loc["2011-04-25 00:00:00":"2011-05-02 00:00:00", "temp_amb"].plot(ax=axes[0], color="darkblue", linewidth=1, alpha=1)
df_Zehdenick.loc["2011-04-25 00:00:00":"2011-05-02 00:00:00", "temp_amb"].plot(ax=axes[0], color="goldenrod", linewidth=1, alpha=1)
df_Heckelberg.loc["2011-06-28 00:00:00":"2011-07-03 00:00:00", "temp_amb"].plot(ax=axes[1], color="darkblue", linewidth=1, alpha=1)
df_Zehdenick.loc["2011-06-28 00:00:00":"2011-07-03 00:00:00", "temp_amb"].plot(ax=axes[1], color="goldenrod", linewidth=1, alpha=1)
#labeling
axes[0].set_title("missing interval april",fontsize = 10,family="serif")
axes[0].set_ylabel("[°C]", fontsize=10, family="monospace", rotation="horizontal")
axes[0].yaxis.set_label_coords(-0.050, 0.920)
axes[0].legend(["Heckelberg", "Zehdenick"], prop={"family": "serif"})
axes[1].set_title("missing interval july",fontsize = 10,family="serif")
axes[1].set_ylabel("[°C]", fontsize=10, family="monospace", rotation="horizontal")
axes[1].yaxis.set_label_coords(-0.050, 0.920)
axes[1].legend(["Heckelberg", "Zehdenick"], prop={"family": "serif"})
plt.tight_layout()
plt.savefig("plots/Heckelberg_missingintervals.jpg", format="jpg")
#plt.show()

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

# Erkner = Berlin-Kaniswall
data = {"temp_amb": {},
        "temp_soil": {}
}
df_Erkner = pd.DataFrame(data,index=date_range)
df_Erkner.loc[:,["temp_amb", "temp_soil"]] = df_Berlin_Kaniswall.loc[:,["temp_amb", "temp_soil"]]
df_Erkner.insert(0,"ags_id", np.full(len(date_range),12067124))

# Grünheide (Mark) -> Berlin-Kaniswall/Müncheberg arithmetic mean
df_Grünheide_Mark = (df_Berlin_Kaniswall + df_Müncheberg)/2
df_Grünheide_Mark.insert(0,"ags_id",np.full(len(date_range),12067201))

# --------------------------------------------------------------------------------------------------------------------->
# all cities are located in different federal states (Bundesländern)
    # create script, which deliver DataFrame contains values about weatherstations closest to a certain geo point

# load Dataframe with all waetherstations, which deliver values for t_amb
    # source: https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/air_temperature/historical/
weatherstations_t_amb = pd.read_csv(r"Wetterstationen\TU_Stundenwerte_Beschreibung_Stationen_t_amb.csv",
                                    encoding='latin1', sep=";")
# cities
position_cities = {
    "Ingolstadt": {"lon": 11.4237, "lat": 48.766, "ags_id": "09161000"},  # IN
    "Kassel": {"lon": 9.479, "lat": 51.312, "ags_id": "06611000"},        # KS
    "Bocholt": {"lon": 6.614, "lat": 51.838, "ags_id": "05554008"},       # BOH
    "Kiel": {"lon": 10.123, "lat": 54.322, "ags_id": "01002000"},         # KI
    "Zwickau": {"lon": 12.461, "lat": 50.706, "ags_id": "14524330"},      # Z
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
            # df_distance with column "Distance" in [km]
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
# DATA -> Ingolstadt
weatherstations_IN = closestweatherstations(position_cities["Ingolstadt"]["lat"],position_cities["Ingolstadt"]["lon"])

#print("Closest weather stations for t_amb near Ingolstadt")
#print(weatherstations_IN.head(8))
# closest weatherstation is "Kösching" --> set as t_amb - Ingolstadt
    # -> missing data in t_amb 13.02.2011-11:00	-> 14.02.2011-00:00	[14]
    # look to weatherstations nearby
        # Ingolstadt-Manching -> missing values in same time
        # Karlshuld -> not in operation anymore
        # Königsmoos-Untermaxfeld -> not in operation anymore
    # -> missing values in t_soil 13.02.2011-09:00 -> 14.02.2011-07:00 [23]

Kösching_raw_amb = pd.read_csv(r"Temperatures_rawdata\Städte\Ingolstadt\Kösching_Temp_amb\produkt_tu_stunde_20041201_20221231_02700.txt",
                               index_col = 1, sep=";")
Kösching_raw_soil = pd.read_csv(r"Temperatures_rawdata\Städte\Ingolstadt\Kösching_Temp_soil\produkt_eb_stunde_19870101_20221231_02700.txt",
                                index_col = 1, sep=";")
Neuburg_raw_amb = pd.read_csv(r"Temperatures_rawdata\Städte\Ingolstadt\Neuburg_Temp_amb\produkt_tu_stunde_20020101_20221231_03484.txt",
                              index_col = 1, sep=";")
Gelbelsee_raw_amb = pd.read_csv(r"Temperatures_rawdata\Städte\Ingolstadt\Gelbelsee_Temp_amb\produkt_tu_stunde_19910101_20221231_01587.txt",
                                index_col = 1, sep=";")
Eichstätt_Landershofen_raw_amb = pd.read_csv(r"Temperatures_rawdata\Städte\Ingolstadt\Eichstätt-Landershofen_Temp_amb\produkt_tu_stunde_20050201_20221231_01161.txt",
                                              index_col = 1, sep=";")

#closest_Kösching = closestweatherstations(11.4872,48.8302)
# create empty dataframes
data = {"temp_amb": {},
        "temp_soil": {}
}
df_Kösching = pd.DataFrame(data, index=date_range)
df_Neuburg = pd.DataFrame(data, index=date_range) # also missing values in Neuburg_raw_amb -> df_temperatures_2011(df_raw_amb,df_raw_soil) not running
df_Gelbelsee = pd.DataFrame(data, index=date_range)
df_Eichstätt_Landershofen = pd.DataFrame(data, index=date_range)

# fill dataframe df_Kösching with known values
df_Kösching.loc["2011-01-01 00:00:00":"2011-02-13 10:00:00", "temp_amb"] = Kösching_raw_amb.loc[2011010100:2011021310, 'TT_TU'].values
df_Kösching.loc["2011-02-14 01:00:00":"2011-12-31 23:00:00", "temp_amb"] = Kösching_raw_amb.loc[2011021401:2011123123, 'TT_TU'].values
df_Kösching.loc["2011-01-01 00:00:00":"2011-02-13 08:00:00", "temp_soil"] = Kösching_raw_soil.loc[2011010100:2011021308, 'V_TE100'].values
df_Kösching.loc["2011-02-14 08:00:00":"2011-12-31 23:00:00", "temp_soil"] = Kösching_raw_soil.loc[2011021408:2011123123, 'V_TE100'].values
# fill dataframes of other near weatherstations with data around the missing interval of t_amb for plotting
df_Eichstätt_Landershofen.loc["2011-02-12 05:00:00":"2011-02-15 07:00:00", "temp_amb"] = Eichstätt_Landershofen_raw_amb.loc[2011021205:2011021507, 'TT_TU'].values
df_Neuburg.loc["2011-02-12 05:00:00":"2011-02-15 07:00:00", "temp_amb"] = Neuburg_raw_amb.loc[2011021205:2011021507, 'TT_TU'].values
df_Gelbelsee.loc["2011-02-12 05:00:00":"2011-02-15 07:00:00", "temp_amb"] = Gelbelsee_raw_amb.loc[2011021205:2011021507, 'TT_TU'].values
# interpolation for missing values
df_inter = (df_Neuburg + df_Gelbelsee)/2

# replace missing values for t_amb in df_Köschling
    # it seems that weatherstation delivered faulty measures before and after missing interval -> sea plot
# plot
fig, axes = plt.subplots(2, 1, figsize=(12, 8))
fig.suptitle(" Weather Station Köching (Ingolstadt) \n Replacement t_amb missing interval february",fontsize=12,family="serif")
df_Kösching.loc["2011-02-12 05:00:00":"2011-02-15 07:00:00", "temp_amb"].plot(ax=axes[0], color="darkblue", linewidth=1, alpha=1)
df_Neuburg.loc["2011-02-12 05:00:00":"2011-02-15 07:00:00", "temp_amb"].plot(ax=axes[0], color="goldenrod", linewidth=1, alpha=1)
df_Gelbelsee.loc["2011-02-12 05:00:00":"2011-02-15 07:00:00", "temp_amb"].plot(ax=axes[0], color="forestgreen", linewidth=1, alpha=1)
df_inter.loc["2011-02-12 05:00:00":"2011-02-15 07:00:00", "temp_amb"].plot(ax=axes[0], color="black", linewidth=1, alpha=1, linestyle="--")
df_Eichstätt_Landershofen.loc["2011-02-12 05:00:00":"2011-02-15 07:00:00", "temp_amb"].plot(ax=axes[0], color="darkviolet", linewidth=1, alpha=1, linestyle=":")
# -> replace values in a bigger interval with interpolation between Neuburg Gelbelsee
df_Kösching.loc["2011-02-13 04:00:00":"2011-02-14 07:00:00", "temp_amb"] = df_inter.loc["2011-02-13 03:00:00":"2011-02-14 07:00:00", "temp_amb"]

df_Kösching.loc["2011-02-12 05:00:00":"2011-02-15 07:00:00", "temp_amb"].plot(ax=axes[1], color="darkblue", linewidth=1, alpha=1)
df_Neuburg.loc["2011-02-12 05:00:00":"2011-02-15 07:00:00", "temp_amb"].plot(ax=axes[1], color="goldenrod", linewidth=1, alpha=1)
df_Gelbelsee.loc["2011-02-12 05:00:00":"2011-02-15 07:00:00", "temp_amb"].plot(ax=axes[1], color="forestgreen", linewidth=1, alpha=1)
df_inter.loc["2011-02-12 05:00:00":"2011-02-15 07:00:00", "temp_amb"].plot(ax=axes[1], color="black", linewidth=1, alpha=1, linestyle="--")
df_Eichstätt_Landershofen.loc["2011-02-12 05:00:00":"2011-02-15 07:00:00", "temp_amb"].plot(ax=axes[1], color="darkviolet", linewidth=1, alpha=1, linestyle=":")
# labeling
#axes[0].set_title("Replacement missing t_amb interval Kösching february",fontsize=10,family="serif")
axes[0].set_ylabel("[°C]", fontsize=10, family="monospace", rotation="horizontal")
axes[0].yaxis.set_label_coords(-0.040, 0.920)
axes[0].legend(["Kösching = Ingolstadt", "Neuburg", "Gelbelsee", "Neuburg/Gelbelsee (mean)", "Eichstätt-Landershofen"],
            prop={"family": "serif"})
axes[1].set_ylabel("[°C]", fontsize=10, family="monospace", rotation="horizontal")
axes[1].yaxis.set_label_coords(-0.040, 0.920)
axes[1].legend(["Kösching = Ingolstadt", "Neuburg", "Gelbelsee", "Neuburg/Gelbelsee (mean)", "Eichstätt-Landershofen"],
            prop={"family": "serif"})
plt.tight_layout()
plt.savefig("plots/Kösching_missingintervals.jpg", format="jpg")
#plt.show()
# interpolate missing values for temp_soil
missing_start_date = "2011-02-13 09:00:00"
missing_end_date = "2011-02-14 07:00:00"
approximate(df_Kösching, missing_start_date, missing_end_date)
# check -> df_Kösching.loc["2011-02-07 09:00:00":"2011-02-21 07:00:00","temp_soil"].plot()

# Ingolstadt = Kösching
data = {"temp_amb": {},
        "temp_soil": {}
}
df_Ingolstadt = pd.DataFrame(data,index=date_range)
df_Ingolstadt.loc[:,["temp_amb", "temp_soil"]] = df_Kösching.loc[:,["temp_amb", "temp_soil"]]
df_Ingolstadt.insert(0,"ags_id", np.full(len(date_range),position_cities["Ingolstadt"]["ags_id"]))

# Test if columns are full
# df_Ingolstadt.loc[:,"temp_amb"].isna().unique()
# df_Ingolstadt.loc[:,"temp_soil"].isna().unique()

# --------------------------------------------------------------------------------------------------------------------->
# DATA -> Kassel
weatherstations_KS = closestweatherstations(position_cities["Kassel"]["lat"],position_cities["Kassel"]["lon"])
#print("Closest weather stations for t_amb near Kassel")
#print(weatherstations_KS.head(8))

# closest weatherstation is "Kassel" --> set as t_amb - Kassel
    # -> missing data interval in temp_amb 24.08.2011-19:00 -> 29.08.2011-08:00    [110]
    # look at weatherstations nearby
        # Schauenburg-Elgershausen --> in operation since 2013
        # Fritzlar/Eder         --> one missing timestamp in interval 25.08.2011-05:00  [1]
        # Warburg               --> no missing values
        # Wesertal-Lippoldsberg --> no missing values
        # Eschwege              --> no missing values
    # -> missing data interval in temp_soil 24.08.2011-19:00 -> 29.08.2011-08:00	[110]

Kassel_raw_amb = pd.read_csv(r"Temperatures_rawdata\Städte\Kassel\Kassel_Temp_amb\produkt_tu_stunde_19480101_20131031_02532.txt",
                             index_col=1, sep=";")
Kassel_raw_soil = pd.read_csv(r"Temperatures_rawdata\Städte\Kassel\Kassel_Temp_soil\produkt_eb_stunde_19770101_20131031_02532.txt",
                              index_col=1, sep=";")
Fritzlar_Eder_raw_amb = pd.read_csv(r"Temperatures_rawdata\Städte\Kassel\Fritzlar_Eder_Temp_amb\produkt_tu_stunde_20020101_20221231_01504.txt",
                                    index_col=1, sep=";")
Fritzlar_Eder_raw_soil = pd.read_csv(r"Temperatures_rawdata\Städte\Kassel\Fritzlar_Eder_Temp_soil\produkt_eb_stunde_20010403_20221231_01504.txt",
                                    index_col=1, sep=";")
Warburg_raw_amb = pd.read_csv(r"Temperatures_rawdata\Städte\Kassel\Warburg_Temp_amb\produkt_tu_stunde_20010402_20221231_05347.txt",
                              index_col=1, sep=";")
Warburg_raw_soil = pd.read_csv(r"Temperatures_rawdata\Städte\Kassel\Warburg_Temp_soil\produkt_eb_stunde_19880201_20221231_05347.txt",
                              index_col=1, sep=";")
Wesertal_Lippoldsberg_raw_amb = pd.read_csv(r"Temperatures_rawdata\Städte\Kassel\Wesertal-Lippoldsberg_Temp_amb\produkt_tu_stunde_20040901_20221231_05279.txt",
                                            index_col=1, sep=";")
Eschwege_raw_amb = pd.read_csv(r"Temperatures_rawdata\Städte\Kassel\Eschwege_Temp_amb\produkt_tu_stunde_20041001_20221231_01297.txt",
                               index_col=1, sep=";")
# create empty dataframes
data = {"temp_amb": {},
        "temp_soil": {}
}
df_Kassel = pd.DataFrame(data, index=date_range)
df_Fritzlar_Eder = pd.DataFrame(data, index=date_range) # also missing values in Neuburg_raw_amb -> df_temperatures_2011(df_raw_amb,df_raw_soil) not running
df_Warburg = pd.DataFrame(data, index=date_range)
df_Wesertal_Lippoldsberg = pd.DataFrame(data, index=date_range)
df_Eschwege = pd.DataFrame(data, index=date_range)

# fill dataframe df_Kassel with known values
df_Kassel.loc["2011-01-01 00:00:00":"2011-08-24 18:00:00", "temp_amb"] = Kassel_raw_amb.loc[2011010100:2011082418, 'TT_TU'].values
df_Kassel.loc["2011-08-29 09:00:00":"2011-12-31 23:00:00", "temp_amb"] = Kassel_raw_amb.loc[2011082909:2011123123, 'TT_TU'].values
df_Kassel.loc["2011-01-01 00:00:00":"2011-08-24 18:00:00", "temp_soil"] = Kassel_raw_soil.loc[2011010100:2011082418, 'V_TE100'].values
df_Kassel.loc["2011-08-29 09:00:00":"2011-12-31 23:00:00", "temp_soil"] = Kassel_raw_soil.loc[2011082909:2011123123, 'V_TE100'].values

# fill dataframes of other weatherstations with data around the missing interval(s) of t_amb for plotting
df_Fritzlar_Eder.loc["2011-08-18 05:00:00":"2011-08-25 04:00:00", "temp_amb"] = Fritzlar_Eder_raw_amb.loc[2011081805:2011082504, 'TT_TU'].values
df_Fritzlar_Eder.loc["2011-08-25 06:00:00":"2011-09-06 07:00:00", "temp_amb"] = Fritzlar_Eder_raw_amb.loc[2011082506:2011090607, 'TT_TU'].values
# in Fritzlar_Eder we replace the missing value with one timestamp before
df_Fritzlar_Eder.loc["2011-08-25 05:00:00", "temp_amb"] = df_Fritzlar_Eder.loc["2011-08-25 04:00:00", "temp_amb"]
df_Warburg.loc["2011-08-18 05:00:00":"2011-09-06 07:00:00","temp_amb"] = Warburg_raw_amb.loc[2011081805:2011090607, 'TT_TU'].values
df_Wesertal_Lippoldsberg.loc["2011-08-18 05:00:00":"2011-09-06 07:00:00","temp_amb"] = Wesertal_Lippoldsberg_raw_amb.loc[2011081805:2011090607, 'TT_TU'].values
df_Eschwege.loc["2011-08-18 05:00:00":"2011-09-06 07:00:00","temp_amb"] = Eschwege_raw_amb.loc[2011081805:2011090607, 'TT_TU'].values

# ------> temp_amp
# interpolation for missing values
df_inter = (df_Wesertal_Lippoldsberg + df_Fritzlar_Eder)/2

fig, axes = plt.subplots(2, 1, figsize=(12, 8))
#fig.suptitle("Weatherstation Kassel and nearby weatherstaions \n t_amb missing interval august",fontsize=12,family="serif")
df_Kassel.loc["2011-08-18 05:00:00":"2011-09-06 07:00:00", "temp_amb"].plot(ax=axes[0], color="darkblue", linewidth=1, alpha=1)
df_Fritzlar_Eder.loc["2011-08-18 05:00:00":"2011-09-06 07:00:00", "temp_amb"].plot(ax=axes[0], color="red", linewidth=1, alpha=0.6, linestyle="-.")
df_Warburg.loc["2011-08-18 05:00:00":"2011-09-06 07:00:00", "temp_amb"].plot(ax=axes[0], color="forestgreen", linewidth=1, alpha=0.6, linestyle="--")
df_Wesertal_Lippoldsberg.loc["2011-08-18 05:00:00":"2011-09-06 07:00:00", "temp_amb"].plot(ax=axes[0], color="black", linewidth=1, alpha=0.6, linestyle=":")
df_Eschwege.loc["2011-08-18 05:00:00":"2011-09-06 07:00:00", "temp_amb"].plot(ax=axes[0], color="darkviolet", linewidth=1, alpha=0.6, linestyle="-.")

df_Kassel.loc["2011-08-18 05:00:00":"2011-09-06 07:00:00", "temp_amb"].plot(ax=axes[1], color="darkblue", linewidth=1, alpha=1)
df_inter.loc["2011-08-18 05:00:00":"2011-09-06 07:00:00", "temp_amb"].plot(ax=axes[1], color="black", linewidth=1, alpha=0.6, linestyle="--")
# labeling
axes[0].set_title("Weatherstation Kassel and nearby weatherstaions \n t_amb missing interval august",fontsize=12,family="serif")
axes[0].set_ylabel("[°C]", fontsize=10, family="monospace", rotation="horizontal")
axes[0].yaxis.set_label_coords(-0.040, 0.920)
axes[0].legend(["Kassel","Fritzlar_Eder","Warburg","Wesertal_Lippoldsberg","Eschwege"],
               loc='upper right', ncol=2, prop={"family": "serif"})
# instead of loc='upper right' -> bbox_to_anchor=(0.60, 0.8) possible

axes[1].set_title("Weatherstation Kassel and interpolation",fontsize=12,family="serif")
axes[1].set_ylabel("[°C]", fontsize=10, family="monospace", rotation="horizontal")
axes[1].yaxis.set_label_coords(-0.040, 0.920)
axes[1].legend(["Kassel","Wesertal_Lippoldsberg/Fritzlar_Eder (mean)"],
            prop={"family": "serif"})

plt.tight_layout()
plt.savefig("plots/Kassel_missing_interval.jpg", format="jpg")

# plt.show()

# -> missing data interval in t_amb 24.08.2011-19:00 -> 29.08.2011-08:00    [110]
# replace missing values in df_Kassel["temp_amb"] with interpolation
df_Kassel.loc["2011-08-24 19:00:00":"2011-08-29 08:00:00", "temp_amb"] = df_inter.loc["2011-08-24 19:00:00":"2011-08-29 08:00:00", "temp_amb"]

# ------> temp_soil
# -> missing data interval in temp_soil 24.08.2011-19:00 -> 29.08.2011-08:00	[110]

# interpolate missing values for temp_soil
missing_start_date = "2011-08-24 19:00:00"
missing_end_date = "2011-08-29 08:00:00"
approximate(df_Kassel, missing_start_date, missing_end_date)
# check -> df_Kassel.loc["2011-08-18 19:00:00":"2011-09-04 08:00:00", "temp_soil"].plot()

# check approximation for 24.08.2011-19:00 -> 29.08.2011-08:00  [41]
    # plot around missing interval -> +- 1 week
    # compare with weatherstation Warburg
df_Warburg.loc["2011-08-18 19:00:00":"2011-09-04 08:00:00","temp_soil"] = Warburg_raw_soil.loc[2011081819:2011090408, 'V_TE100'].values

start_date = "2011-08-18 19:00:00"
end_date = "2011-09-04 08:00:00"

fig, axes = plt.subplots(1, 1, figsize=(12, 8))
df_Kassel.loc[start_date:end_date, "temp_soil"].plot(ax=axes, color="darkblue", linewidth=1, alpha=1)
df_Warburg.loc[start_date:end_date, "temp_soil"].plot(ax=axes, color="goldenrod", linewidth=1, alpha=0.6)
# labeling
axes.set_title("Weatherstation Kassel and Warburg \n temp_soil missing interval august",fontsize=12,family="serif")
axes.set_ylabel("[°C]", fontsize=10, family="monospace", rotation="horizontal")
axes.yaxis.set_label_coords(-0.0550, 0.980)
axes.legend(["Kassel","Warburg"],loc='upper right', prop={"family": "serif"})
#axes.set_facecolor('lavender')
plt.tight_layout()
plt.savefig("plots/Kassel_check_approx.jpg", format="jpg")

# Test if columns are full
# df_Kassel.loc[:,"temp_amb"].isna().unique()
# df_Kassel.loc[:,"temp_soil"].isna().unique()

df_Kassel.insert(0,"ags_id", np.full(len(date_range),position_cities["Kassel"]["ags_id"]))

# --------------------------------------------------------------------------------------------------------------------->
# DATA -> Bocholt

weatherstations_BOH = closestweatherstations(position_cities["Bocholt"]["lat"],position_cities["Bocholt"]["lon"])

    # look at weatherstations nearby
        # Bocholt               --> not in operation anymore
        # Bocholt-Liedern       --> not in operation anymore
        # Borken                --> status ok
        # Kalkar                --> many missing values in 2011
        # Kleve                 --> status ok - temp_soil not available
    # use data from Borken und Kleve -> build mean for temp_amb

Borken_raw_amb = pd.read_csv(r"Temperatures_rawdata\Städte\Bocholt\Borken_Temp_amb\produkt_tu_stunde_20040601_20221231_00617.txt",
                             index_col=1, sep=";")
Borken_raw_soil = pd.read_csv(r"Temperatures_rawdata\Städte\Bocholt\Borken_Temp_soil\produkt_eb_stunde_20040601_20221231_00617.txt",
                              index_col=1, sep=";")
Kleve_raw_amb = pd.read_csv(r"Temperatures_rawdata\Städte\Bocholt\Kleve_Temp_amb\produkt_tu_stunde_20040701_20221231_02629.txt",
                            index_col=1, sep=";")
# collect data for 2011
df_Borken = df_temperatures_2011(Borken_raw_amb,Borken_raw_soil)
df_Kleve = df_temperatures_2011(Kleve_raw_amb,Borken_raw_soil)

# interpolate values for Bocholt with mean between Borken and Kleve
df_Bocholt = (df_Borken + df_Kleve) /2

df_Bocholt.insert(0,"ags_id", np.full(len(date_range),position_cities["Bocholt"]["ags_id"]))
# Test if columns are full
# df_Bocholt.loc[:,"temp_amb"].isna().unique()
# df_Bocholt.loc[:,"temp_soil"].isna().unique()

# --------------------------------------------------------------------------------------------------------------------->
# DATA -> Kiel

weatherstations_KI = closestweatherstations(position_cities["Kiel"]["lat"],position_cities["Kiel"]["lon"])

    # look at weatherstations nearby
        # Kiel-Kronshagen       --> not in operation anymore
        # Kiel-Holtenau         --> temp_amp - >  23.07.2011-05:00 -> 23.07.2011-09:00  [5]  and many 1h-intervals (>10)
                            #   --> temp_soil ->  22.07.2011-08:00 -> 24.07.2011-06:00
        # Ostenfeld             --> status ok -> for replacment
    # use data from Ostenfeld

Kiel_Kronshagen_raw_amb = pd.read_csv(r"Temperatures_rawdata\Städte\Kiel\Kiel_Holtenau_Temp_amb\produkt_tu_stunde_20020101_20221231_02564.txt",
                             index_col=1, sep=";")
Kiel_Kronshagen_raw_soil = pd.read_csv(r"Temperatures_rawdata\Städte\Kiel\Kiel_Holtenau_Temp_soil\produkt_eb_stunde_19860501_20221231_02564.txt",
                             index_col=1, sep=";")
Ostenfeld_raw_amb = pd.read_csv(r"Temperatures_rawdata\Städte\Kiel\Ostenfeld_Temp_amb\produkt_tu_stunde_20040501_20221231_06105.txt",
                             index_col=1, sep=";")
Ostenfeld_raw_soil = pd.read_csv(r"Temperatures_rawdata\Städte\Kiel\Ostenfeld_Temp_soil\produkt_eb_stunde_19980601_20221231_06105.txt",
                             index_col=1, sep=";")
# collect data for 2011
df_Kiel = df_temperatures_2011(Ostenfeld_raw_amb,Ostenfeld_raw_soil)
df_Kiel.insert(0,"ags_id", np.full(len(date_range),position_cities["Kiel"]["ags_id"]))
# Test if columns are full
# df_Kiel.loc[:,"temp_amb"].isna().unique()
# df_Kiel.loc[:,"temp_soil"].isna().unique()

# --------------------------------------------------------------------------------------------------------------------->
# DATA -> Zwickau

weatherstations_Z = closestweatherstations(position_cities["Zwickau"]["lat"],position_cities["Zwickau"]["lon"])

    # look at weatherstations nearby
        # Lichtentanne          --> status ok -> temp_soil not available
        # Treuen                --> status ok
    # use Data from Treuen for temp_soil

Lichtentanne_raw_amb = pd.read_csv(r"Temperatures_rawdata\Städte\Zwickau\Lichtentanne_Temp_amb\produkt_tu_stunde_20051201_20221231_05797.txt",
                             index_col=1, sep=";")
Treuen_raw_soil = pd.read_csv(r"Temperatures_rawdata\Städte\Zwickau\Treuen_Temp_soil\produkt_eb_stunde_20051027_20221231_07329.txt",
                             index_col=1, sep=";")
# collect data for 2011
df_Zwickau = df_temperatures_2011(Lichtentanne_raw_amb,Treuen_raw_soil)
df_Zwickau.insert(0,"ags_id", np.full(len(date_range),position_cities["Zwickau"]["ags_id"]))
# Test if columns are full
# df_Zwickau.loc[:,"temp_amb"].isna().unique()
# df_Zwickau.loc[:,"temp_soil"].isna().unique()

# --------------------------------------------------------------------------------------------------------------------->
# create .csv file

df = pd.concat([df_Rüdersdorf,df_Strausberg,df_Erkner,df_Grünheide_Mark,df_Ingolstadt,df_Kassel,df_Bocholt,df_Kiel,df_Zwickau])
df.sort_index(inplace=True)

data = dict(timestamp=df.index,
            ags_id=df.loc[:, "ags_id"].values,
            temp_amb=df.loc[:, "temp_amb"].values.round(2),
            temp_soil=df.loc[:, "temp_soil"].values.round(2))
temperatures_2011 = pd.DataFrame(data)

temperatures_2011.to_csv("temperatures_2011",index=False)