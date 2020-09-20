import os, sys
from pathlib import Path

# Application root
root_path = Path().absolute()

# Path for storing raw data
data_path = root_path /"preprocess_data" / "data"

aquifers_geojson = data_path / "all_us_aquifers.geojson"
aquifers_shapefile = data_path / "all_us_aquifers/all_us_aquifers.shp"
hydrologic_basin_shapefile = data_path / "pr_hydrologic_basin/pr_hydrologic_basin.shp"

well_data_path = data_path / "well_data"
well_data_path.mkdir(parents=True, exist_ok=True)

rain_data_path = data_path / "rain_data"
rain_data_path.mkdir(parents=True, exist_ok=True)

usgs_well_iv = well_data_path / "usgs_well_iv_data.csv"
usgs_rain_iv = rain_data_path / "usgs_rain_iv_data.csv"
ncei_rain_daily = rain_data_path / "ncei_rain_ghcn_daily_data.csv"

usgs_historical_well_sites_raw = well_data_path / "usgs_historical_well_sites_raw.tsv"
usgs_historical_rain_sites_raw = rain_data_path / "usgs_historical_rain_sites_raw.tsv"
usgs_historical_well_data_raw = well_data_path / "usgs_historical_well_data_raw.tsv"
usgs_historical_rain_data_raw = rain_data_path / "usgs_historical_rain_data_raw.tsv"

usgs_historical_well_sites = well_data_path / "usgs_historical_well_sites.csv"
usgs_historical_rain_sites = rain_data_path / "usgs_historical_rain_sites.csv"
usgs_historical_well_data = well_data_path / "usgs_historical_well_data.csv"
usgs_historical_rain_data = rain_data_path / "usgs_historical_rain_data.csv"

raw_nerr_data_path = data_path / "raw_nerr_data"
nerr_data_path = data_path / "nerr_data"
nerr_wq_data_path = nerr_data_path / "nerr_wq_data.csv"
nerr_met_data_path = nerr_data_path / "nerr_met_data.csv"
nerr_nut_data_path = nerr_data_path / "nerr_nut_data.csv"
nerr_stations_data_path = nerr_data_path / "nerr_sampling_stations.csv"

# Path for storing data profiles...
data_profile = root_path / "data_profile"

# Dropbox hosted csvs...
# nerr_met_url = "https://www.dropbox.com/s/yqtxdgl6nheghq7/nerr_met_data.csv?dl=1"
# nerr_nut_url = "https://www.dropbox.com/s/16z9y1e46f3j23u/nerr_nut_data.csv?dl=1"
# nerr_stations_url = "https://www.dropbox.com/s/rov04m2ue4c4799/nerr_sampling_stations.csv?dl=1"
# nerr_wq_url = "https://www.dropbox.com/s/zi7jvr8qfy7wmmx/nerr_wq_data.csv?dl=1"

# Arcgis Hosted csvs...
nerr_met_url = "https://arac-personal.maps.arcgis.com/sharing/rest/content/items/3358a0ba6e114cffaa47c11b510a5603/data"
nerr_nut_url = "https://arac-personal.maps.arcgis.com/sharing/rest/content/items/d1569071716d4b569e2eee439e7765d5/data"
nerr_stations_url = "https://arac-personal.maps.arcgis.com/sharing/rest/content/items/d6ced9d29ab54337b8b19d35b60feb01/data"
nerr_wq_url = "https://arac-personal.maps.arcgis.com/sharing/rest/content/items/1f27606babee4482a229d4bf4b4163e4/data"
