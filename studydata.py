import pandas as pd
from app_constants import (
    usgs_historical_well_sites,
    usgs_historical_rain_sites,
    usgs_historical_well_data,
    usgs_historical_rain_data,
    aquifers_shapefile,
    hydrologic_basin_shapefile,
    nerr_wq_data_path,
    nerr_met_data_path,
    nerr_nut_data_path,
    nerr_stations_data_path
)
import json
import geopandas as gpd


# from pandas_profiling import ProfileReport
# Module in charge of loading all study data into a user friendly class...
class StudyData:

    RESAMPLE_FREQ = "1H"

    USGS_AGG_WELL = dict(
        water_level="mean",
        # source="first",
        # quality_flag="first"
    )

    USGS_AGG_RAIN = dict(
        precipitation="mean",
        # source="first",
        # quality_flag="first"
    )

    USGS_WELL_RESAMPLE_SETTINGS = dict(
        freq=RESAMPLE_FREQ,
        agg_functions=USGS_AGG_WELL
    )

    USGS_RAIN_RESAMPLE_SETTINGS = dict(
        freq=RESAMPLE_FREQ,
        agg_functions=USGS_AGG_RAIN
    )

    def __init__(self):
        self.usgs_well_historical = None
        self.usgs_rain_historical = None

        self._load_data()

    def _load_data(self):

        site_dtypes = {
            "source": "str",
            "site_id": "str",
            "site_name": "str",
            "latitude": "float64",
            "longitude": "float64",
            "latlng_datum": "str",
            "altitude": "float64",
            "altitude_datum": "str",
            "hydrologic_unit_code": "str",
            "national_aquifer_code": "str",
            "local_aquifer_code": "str"
        }

        well_dtypes = {
            "site_id": "str",
            "water_level": "float64",
            "quality_flag": "str",
            "date_time": "str"
        }

        rain_dtypes = {
            "site_id": "str",
            "precipitation": "float64",
            "quality_flag": "str",
            "date_time": "str"
        }
        parse_dates_col = ["date_time"]

        self.usgs_historical_well_sites = pd.read_csv(
            usgs_historical_well_sites,
            dtype=site_dtypes
        )
        self.usgs_historical_rain_sites = pd.read_csv(
            usgs_historical_rain_sites,
            dtype=site_dtypes
        )

        self.usgs_historical_well_data = pd.read_csv(
            usgs_historical_well_data,
            dtype=well_dtypes,
            usecols=well_dtypes.keys(),
            parse_dates=parse_dates_col

        )
        self.usgs_historical_rain_data = pd.read_csv(
            usgs_historical_rain_data,
            dtype=rain_dtypes,
            usecols=rain_dtypes.keys(),
            parse_dates=parse_dates_col
        )

    def get_usgs_historical_well_sites(self, as_gdf=True):
        df = self.usgs_historical_well_sites.copy()
        df["site_type"] = "Groundwater"
        if as_gdf:
            # Convert to sde
            df = gpd.GeoDataFrame(
                df,
                geometry=(
                    gpd.points_from_xy(df.longitude, df.latitude)
                )
            )
        return df

    def get_usgs_historical_rain_sites(self, as_gdf=True):
        df = self.usgs_historical_rain_sites.copy()
        df["site_type"] = "Meteorological"
        if as_gdf:
            # Convert to sde
            df = gpd.GeoDataFrame(
                df,
                geometry=(
                    gpd.points_from_xy(df.longitude, df.latitude)
                )
            )
        return df

    def get_usgs_historical_well_rain_sites(self, as_gdf=True):
        well = self.get_usgs_historical_well_sites(as_gdf)
        rain = self.get_usgs_historical_rain_sites(as_gdf)

        well_rain = pd.concat([well, rain], ignore_index=True)
        return well_rain

    def get_usgs_historical_well_data(
        self,
        resample_params=None,
    ):
        df = self.usgs_historical_well_data.copy()

        if resample_params:
            df = self._resample_df(df, **resample_params)

        return df

    def get_usgs_historical_rain_data(
        self,
        resample_params=None,
    ):
        df = self.usgs_historical_rain_data.copy()

        if resample_params:
            df = self._resample_df(df, **resample_params)

        return df

    def get_usgs_historical_well_rain_data(
        self,
        freq,
        date_start=None,
        date_end=None
    ):
        agg_functions = dict(water_level="mean")
        resample_params = dict(freq=freq, agg_functions=agg_functions)
        well = self.get_usgs_historical_well_data(
            resample_params=resample_params
        )

        agg_functions = dict(precipitation="mean")
        resample_params = dict(freq=freq, agg_functions=agg_functions)
        rain = self.get_usgs_historical_rain_data(
            resample_params=resample_params
        )

        if date_start and date_end:
            well = self._reindex_df(well, freq, date_start, date_end)
            rain = self._reindex_df(rain, freq, date_start, date_end)

        well_rain = well.merge(
            rain,
            how="left",
            left_on="date_time",
            right_on="date_time",
            suffixes=("_well", "_rain")
        )

        return well_rain

    def _resample_df(self, df, freq, agg_functions):
        # resample usgs to hourly
        grouper_list = [
            pd.Grouper(level="site_id"),
            pd.Grouper(level="date_time", freq=freq)
        ]
        df = df.set_index(["site_id", "date_time"]).sort_index()
        df = df.groupby(grouper_list).agg(agg_functions)
        df = df.reset_index()
        return df

    def _reindex_df(self, df, freq, date_start, date_end):
        df = df.set_index(["site_id", "date_time"]).sort_index()
        date_index = pd.date_range(
            date_start, date_end, freq=freq).rename('date_time')
        idx2 = pd.MultiIndex.from_product(
            [df.index.get_level_values('site_id').unique(), date_index])
        df2 = df.reindex(idx2)
        df2 = df2.reset_index()
        return df2

    def get_aquifers_df(self):
        df = gpd.read_file(aquifers_shapefile)
        fields = [
            "AQ_NAME",
            "AQ_CODE",
            "ROCK_NAME",
            "ROCK_TYPE",
            "geometry",
            "Shape_Leng",
            "Shape_Area"
        ]
        df = df[fields]

        df.columns = [col.lower() for col in df.columns]
        df = df.rename({"shape_leng": "shape_length"}, axis=1)
        return df

    def get_hydrologic_basin_df(self):
        df = gpd.read_file(hydrologic_basin_shapefile)

        fields = [
            "HUC10",
            "Name",
            "States",
            "AreaSqKm",
            "geometry",
            "Shape_Leng",
            "Shape_Area"
        ]
        df = df[fields]
        df.columns = [col.lower() for col in df.columns]
        return df

    # def create_data_profile(
    #     self,
    #     df,
    #     notebook_display=True,
    #     output=None,
    #     title="Pandas Profile",
    #     progress_bar=True
    # ):
    #     prof = ProfileReport(
    #         df,
    #         title=title,
    #         progress_bar=progress_bar
    #     )
    #     if output:
    #         prof.to_file(output)
    #     if notebook_display:
    #         prof.to_widgets()
    #     # return prof

    # def create_raw_data_profiles(
    #     self,
    #     transform=False,
    #     notebook_display=False,
    #     progress_bar=False
    # ):
    #     usgs_rain_df = self.get_usgs_rain_iv(transform)
    #     usgs_well_df = self.get_usgs_well_iv(transform)
    #     ncei_rain_df = self.get_ncei_rain_ghcn_daily(transform)
    #     print("Generating profiles for raw data...")
    #     output = data_profile / "raw_usgs_rain_iv_profile.html"
    #     self.create_data_profile(
    #         usgs_rain_df,
    #         notebook_display=notebook_display,
    #         output=output,
    #         title="USGS Rain IV Pofile",
    #         progress_bar=progress_bar
    #     )
    #     output = data_profile / "raw_usgs_well_iv_profile.html"
    #     self.create_data_profile(
    #         usgs_well_df,
    #         notebook_display=notebook_display,
    #         output=output,
    #         title="USGS Well IV Pofile",
    #         progress_bar=progress_bar
    #     )
    #     output = data_profile / "raw_ncei_rain_daily_profile.html"
    #     self.create_data_profile(
    #         ncei_rain_df,
    #         notebook_display=notebook_display,
    #         output=output,
    #         title="NCEI Rain Daily Pofile",
    #         progress_bar=progress_bar
    #     )
    #     print("Done...")


class NerrStudyData:

    def __init__(self):
        self.nerr_wq_data = self._load_wq_data()
        self.nerr_met_data = self._load_met_data()
        self.nerr_nut_data = self._load_nut_data()
        self.nerr_stations = self._load_stations()

    def _read_csv(self, csv_path, dtypes, usecols):
        df = pd.read_csv(
            csv_path,
            dtype=dtypes,
            usecols=dtypes.keys()
        )
        return df

    def _preprocess_data(self, df, datecols, fmt):
        for col in datecols:
            df[col] = pd.to_datetime(df[col], format=fmt)

        return df

    def _load_wq_data(self):
        dtypes = {
            "StationCode": "str",
            "DateTimeStamp": "str",
            "Historical": "str",
            "ProvisionalPlus": "str",
            "Temp": "float64",
            "F_Temp": "str",
            "SpCond": "float64",
            "F_SpCond": "str",
            "Sal": "float64",
            "F_Sal": "str",
            "DO_Pct": "float64",
            "F_DO_Pct": "str",
            "DO_mgl": "float64",
            "F_DO_mgl": "str",
            "Depth": "float64",
            "F_Depth": "str",
            "cDepth": "float64",
            "F_cDepth": "str",
            "pH": "float64",
            "F_pH": "str",
            "Turb": "float64",
            "F_Turb": "str",
            "ChlFluor": "float64",
            "F_ChlFluor": "str"
        }

        df = self._read_csv(
            nerr_wq_data_path,
            dtypes,
            dtypes.keys()
        )
        datecols = ["DateTimeStamp"]
        fmt = r"%m/%d/%Y %H:%M"
        df = self._preprocess_data(df, datecols, fmt)
        return df

    def _load_met_data(self):
        dtypes = {
            'StationCode': "str",
            'DateTimeStamp': "str",
            'Historical': "str",
            'ProvisionalPlus': "str",
            'Frequency': "str",
            'ATemp': "float64",
            'F_ATemp': "str",
            'RH': "float64",
            'F_RH': "str",
            'BP': "float64",
            'F_BP': "str",
            'WSpd': "float64",
            'F_WSpd': "str",
            'MaxWSpd': "float64",
            'F_MaxWSpd': "str",
            'MaxWSpdT': "str",
            'Wdir': "float64",
            'F_Wdir': "str",
            'SDWDir': "float64",
            'F_SDWDir': "str",
            'TotPAR': "float64",
            'F_TotPAR': "str",
            'TotPrcp': "float64",
            'F_TotPrcp': "str",
        }

        df = self._read_csv(
            nerr_met_data_path,
            dtypes,
            dtypes.keys()
        )
        datecols = ["DateTimeStamp"]
        fmt = r"%m/%d/%Y %H:%M"
        df = self._preprocess_data(df, datecols, fmt)
        return df

    def _load_nut_data(self):
        dtypes = {
            'StationCode': "str",
            'DateTimeStamp': "str",
            'Historical': "str",
            'ProvisionalPlus': "str",
            'PO4F': "float",
            'F_PO4F': "str",
            'NH4F': "float",
            'F_NH4F': "str",
            'NO2F': "float",
            'F_NO2F': "str",
            'NO3F': "float",
            'F_NO3F': "str",
            'NO23F': "float",
            'F_NO23F': "str",
            'CHLA_N': "float",
            'F_CHLA_N': "str",
        }

        df = self._read_csv(
            nerr_nut_data_path,
            dtypes,
            dtypes.keys()
        )
        datecols = ["DateTimeStamp"]
        fmt = r"%m/%d/%Y %H:%M"
        df = self._preprocess_data(df, datecols, fmt)
        return df

    def _load_stations(self):
        dtypes = {
            'StationCode': "str",
            'StationName': "str",
            'Latitude': "float64",
            'Longitude': "float64",
            'Status': "str",
            'ActiveDates': "str",
            'State': "str",
            'ReserveName': "str",
            'GMTOffset': "str",
        }

        df = self._read_csv(
            nerr_stations_data_path,
            dtypes,
            dtypes.keys()
        )

        # For some reason, Puerto Rico and probably other stations`
        # longitude lacks the negative sign...
        def correct_coordinates(df):
            mask = (df["State"] == "pr")
            df.loc[mask, "Longitude"] *= -1
            return df

        df = correct_coordinates(df)
        def classify_station(station_code):

            if "met" in station_code:
                station_type = "Meteorological"
            elif "nut" in station_code:
                station_type = "Nutrients"
            elif "wq" in station_code:
                station_type = "Water Quality"
            else:
                station_type = "Unknown"
            return station_type

        df["StationType"] = df.StationCode.apply(lambda x: classify_station(x))
        df

        return df

    def get_stations(self, as_gdf=True, pr_only=True):
        df = self.nerr_stations.copy()
        if as_gdf:
            # Convert to sde
            df = gpd.GeoDataFrame(
                df,
                geometry=(
                    gpd.points_from_xy(df["Longitude"], df["Latitude"])
                )
            )
        if pr_only:
            mask = (df["State"] == "pr")
            df = df.loc[mask]
        return df

    def get_wq_data(
        self,
        resample_params=None,
    ):
        df = self.nerr_wq_data.copy()

        if resample_params:
            df = self._resample_df(df, **resample_params)

        return df

    def get_met_data(
        self,
        resample_params=None,
    ):
        df = self.nerr_met_data.copy()

        if resample_params:
            df = self._resample_df(df, **resample_params)

        return df

    def get_nut_data(
        self,
        resample_params=None,
    ):
        df = self.nerr_nut_data.copy()

        if resample_params:
            df = self._resample_df(df, **resample_params)

        return df
