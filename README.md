# Temperaturen

- Anhand von Daten des deutschen Wetterdienstes werden für verschiedene Standorte die Jahrezeitreihen für die Umgebungstemperatur, bzw. Lufttemperatur temp_amb und die Bodentemperatur bei einer Bodentiefe temp_soil von 1m ermittelt.
- die geographischen Mittelpunkte können mit google maps approximiert werden, bzw. können mit folgender Funktion berechnet werden, <br>
  wobei gdf die geometrien der Landkreise enthält:

```
  gdf =r"Datafolder\DE_VG250.gpkg"

  regions = ["Rüdersdorf bei Berlin", "Strausberg", "Erkner", "Grünheide (Mark)",
             "Kiel", "Ingolstadt", "Kassel", "Bocholt", "Zwickau"]
  
  def get_position(gdf,region): 
      df = gpd.read_file(gdf) 
      points_of_muns = df.loc[df.loc[df.GEN == region].index,"geometry"].head(1).centroid.values 
      points_of_muns_crs = points_of_muns.to_crs(4326) 
   
      return points_of_muns_crs 
  
  center_positions = [ ] 
  for region in regions: 
      center_positions.append(get_position(gdf,region)) 
    
```
- Daten zu den Wetterstationen können abgerufen werden über:<br>
https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/

- Für eine Region wird jeweils die nächstgelegende Wetterstation gewählt
    - gibt es in unmittelbarer Nähe keine Wetterstation muss gegebenfalls zwischen den Daten von mehreren Wetterstationen interpoliert werden

- fehlende Daten für temp_amb können mit benachbarten Wetterstation ersetzt, bzw. interpoliert werden,
- fehlende Daten für temp_soil können in der Regel linear approximiert werden. Zeitintervalle meist klein genug, dass sich die Monotonie nicht ändert.
    - bei größeren Zeitintervallen (> 2 Tage) Temperaturverlauf mit benachbarter Wetterstation prüfen
