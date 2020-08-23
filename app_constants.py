import os, sys
from pathlib import Path

# Application root
root_path = Path().absolute()

# Path for storing raw data
data_path = root_path / "data"

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