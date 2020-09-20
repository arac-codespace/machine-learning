import pandas as pd
from data_constants import (
    usgs_historical_well_sites_raw,
    usgs_historical_rain_sites_raw,
    usgs_historical_well_data_raw,
    usgs_historical_rain_data_raw,
    usgs_historical_well_sites,
    usgs_historical_rain_sites,
    usgs_historical_well_data,
    usgs_historical_rain_data
)
# from pandas_profiling import ProfileReport
# Module in charge of transforming usgs data...
class USGSProcessing:

    USGS_WELL_DATA_COLS = {
        "site_no": "site_id",
        "datetime": "date_time",
        # "tz_cd": "timezone",
        "165603_72019": "water_level",
        "165603_72019_cd": "quality_flag",
        "agency_cd": "source"
    }

    USGS_RAIN_DATA_COLS = {
        "site_no": "site_id",
        "datetime": "date_time",
        # "tz_cd": "timezone",
        "123818_00045": "precipitation",
        "123818_00045_cd": "quality_flag",
        "agency_cd": "source"
    }

    USGS_SITES_COLS = {
        "agency_cd": "source",
        "site_no": "site_id",
        "station_nm": "site_name",
        "dec_lat_va": "latitude",
        "dec_long_va": "longitude",
        # "coord_acy_cd": "latlng_accuracy",
        "coord_datum_cd": "latlng_datum",
        "alt_va": "altitude",
        # "alt_acy_va": "altitude_accuracy",
        "alt_datum_cd": "altitude_datum",
        "huc_cd": "hydrologic_unit_code",
        # "basin_cd": "drainage_basin_code",
        # "drain_area_va": "drainage_area",
        "nat_aqfr_cd": "national_aquifer_code",
        "aqfr_cd": "local_aquifer_code",
        # "well_depth_va": "well_depth",
        # "hole_depth_va": "hole_depth"
    }

    def __init__(self):
        self.usgs_well_historical = None
        self.usgs_rain_historical = None

        self._load_data()

    def _load_data(self):
        site_cols = self.USGS_SITES_COLS
        well_cols = self.USGS_WELL_DATA_COLS
        rain_cols = self.USGS_RAIN_DATA_COLS
        # https://waterdata.usgs.gov/nwis/gwlevels/help?codes_help#ground_water
        # Really usgs? you going to include error codes in a
        # numerical column?  What's that quality col for
        # yo?
        # Eqp for equipment malfunction...
        na_values = ["Eqp"]
        self.usgs_historical_well_sites = pd.read_csv(
            usgs_historical_well_sites_raw,
            comment="#",
            sep='\t',
            low_memory=False,
            usecols=site_cols
        )
        self.usgs_historical_rain_sites = pd.read_csv(
            usgs_historical_rain_sites_raw,
            comment="#",
            sep='\t',
            low_memory=False,
            usecols=site_cols
        )

        self.usgs_historical_well_data = pd.read_csv(
            usgs_historical_well_data_raw,
            comment="#",
            sep='\t',
            low_memory=False,
            usecols=well_cols,
            na_values=na_values
        )
        self.usgs_historical_rain_data = pd.read_csv(
            usgs_historical_rain_data_raw,
            comment="#",
            sep='\t',
            low_memory=False,
            usecols=rain_cols,
            na_values=na_values
        )

    @classmethod
    def process_and_save_data(cls):
        studydata = cls()
        print("Processing well data...")
        usgs_well = studydata.get_usgs_historical_well_data()
        usgs_well.to_csv(usgs_historical_well_data, index=False)
        print("Processing rain data...")
        usgs_rain = studydata.get_usgs_historical_rain_data()
        usgs_rain.to_csv(usgs_historical_rain_data, index=False)
        print("Processing well site metadata...")
        usgs_well_sites = studydata.get_usgs_historical_well_sites()
        usgs_well_sites.to_csv(usgs_historical_well_sites, index=False)
        print("Processing rain site metadata...")
        usgs_rain_sites = studydata.get_usgs_historical_rain_sites()
        usgs_rain_sites.to_csv(usgs_historical_rain_sites, index=False)

    def get_usgs_historical_well_data(
        self,
        original=False
    ):
        df = self.usgs_historical_well_data.copy()
        if original:
            return df

        # provide rename dictionary...
        rename_cols = self.USGS_WELL_DATA_COLS
        drop_na_subset = ["water_level"]
        df = self._transform_usgs_historical_data(
            df, rename_cols, drop_na_subset)
        float_cols = ["water_level"]
        category_cols = ["site_id", "source", "quality_flag"]
        df = self._change_dtypes(df, float_cols, category_cols)
        return df

    def get_usgs_historical_rain_data(
        self,
        original=False
    ):
        df = self.usgs_historical_rain_data.copy()
        if original:
            return df

        # provide rename dictionary...
        rename_cols = self.USGS_RAIN_DATA_COLS

        drop_na_subset = ["precipitation"]
        df = self._transform_usgs_historical_data(
            df, rename_cols, drop_na_subset)

        float_cols = ["precipitation"]
        category_cols = ["site_id", "source", "quality_flag"]
        df = self._change_dtypes(df, float_cols, category_cols)
        return df

    def get_usgs_historical_well_sites(
        self,
        original=False
    ):
        df = self.usgs_historical_well_sites.copy()
        if original:
            return df

        # provide rename dictionary...
        rename_cols = self.USGS_SITES_COLS

        df = self._transform_usgs_historical_sites(df, rename_cols)
        return df

    def get_usgs_historical_rain_sites(
        self,
        original=False
    ):
        df = self.usgs_historical_rain_sites.copy()
        if original:
            return df

        # provide rename dictionary...
        rename_cols = self.USGS_SITES_COLS

        df = self._transform_usgs_historical_sites(df, rename_cols)
        return df

    # Transforms usgs data into a common format
    def _transform_usgs_historical_sites(self, df, rename_cols):
        # Remove first row that contains useless data...
        df = df.drop([0])
        # Keep columns that appear in the rename argument
        df = df.rename(columns=rename_cols)

        df["site_id"] = df["site_id"].astype(str)
        # df["source"] = df["source"].astype(str)
        return df

    def _change_dtypes(self, df, float_cols=[], category_cols=[]):
        for col in category_cols:
            df[col] = df[col].astype("str")
        for col in float_cols:
            df[col] = df[col].astype("float32")

        return df

    # Transforms usgs data into a common format
    def _transform_usgs_historical_data(
        self,
        df,
        rename_cols,
        drop_na_subset,
    ):
        # Remove first row that contains useless data...
        df = df.drop([0])

        df = df.rename(columns=rename_cols)
        df.dropna(subset=drop_na_subset, inplace=True)
        df = df.sort_values(by=["site_id", "date_time"])
        df = df.drop_duplicates(keep="last")
        df["date_time"] = pd.to_datetime(
            df["date_time"],
            errors="coerce"
        ).dt.tz_localize(None)
        df.dropna(subset=["date_time"], inplace=True)
        return df


if __name__ == "__main__":
    usgs = USGSProcessing()
    usgs.process_and_save_data()

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
