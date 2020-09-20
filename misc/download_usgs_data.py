import os

import pandas as pd
from arcgis.features import GeoAccessor, GeoSeriesAccessor, FeatureLayer

from data_constants import usgs_well_csv, usgs_rain_csv
from web_data_services.web_services.usgs import USGS
from web_data_services.preprocessing.parse_usgs import USGSParser


class UsgsStudyData:

    well_query_params = {
        "stateCd": "PR",
        "localAquiferCd": "PR:110SCPL",
        "parameterCd": "72019",  # depth to water level in ft
        # "seriesCatalogOutput": "true",
        "hasDataTypeCd": "iv",  # time series recorded by devices...
        "format": "rdb"
    }

    rain_query_params = {
        # "stateCd": "PR",
        "huc": "21010004",
        "parameterCd": "00045",  # depth to water level in ft
        # "seriesCatalogOutput": "true",
        "hasDataTypeCd": "iv",  # time series recorded by devices...
        "format": "rdb"
    }

    # Dates and codes used for getting data from the iv endpoint...
    gw_depth_cd = "72019"  # groundwater depth ft.
    rain_cd = "00045"  # precipitation in.

    def __init__(self):
        self.service = None
        self.parser = None

        self._set_service_parser()

    # Initialize the service and parser objects...
    def _set_service_parser(self):
        service = USGS()
        parser = USGSParser()
        self.service = service
        self.parser = parser

    # Get location info from the site endpoint
    def get_location_information(self, query_params):
        service = self.service
        parser = self.parser
        endpoint = "site/"

        # This function returns the response object from requests
        response = service.make_get_request(endpoint, **query_params)
        response.content
        data = parser.parse_sites_response(response)
        sites = pd.DataFrame(data)
        sites["latitude"] = pd.to_numeric(sites["latitude"])
        sites["longitude"] = pd.to_numeric(sites["longitude"])

        sites = pd.DataFrame.spatial.from_xy(
            df=sites,
            x_column="longitude",
            y_column="latitude",
        )
        return sites

    # Get data from the instantaneous values endpoint
    def get_site_data(self, site_id, date_start, date_end, parameter_cd):
        service = self.service
        parser = self.parser
        endpoint = "iv/"

        query_params = {
            "startDT": date_start,
            "endDT": date_end,
            "site": site_id,
            "parameterCd": parameter_cd,  # depth to water level in ft
            "format": "json"
        }

        # This function returns the response object from requests
        response = service.make_get_request(endpoint, **query_params)
        data = parser.parse_iv_response(response)
        print("Done")
        data = pd.DataFrame(data)
        return data

    def get_hydrologic_basin_polygon(self):
        # Load hydrologic basin fc...
        hb_path = r"C:\Users\alexa\Documents\ArcGIS\Projects\machine-learning-map\machine-learning-map.gdb\pr_hydrologic_basin"
        hydrologic_basin = pd.DataFrame().spatial.from_featureclass(hb_path)
        return hydrologic_basin

    def get_study_polygon(self, huc_number="2101000404"):
        hydrologic_basin = self.get_hydrologic_basin_polygon()
        # Get study area polygon
        study_basin = hydrologic_basin[hydrologic_basin["HUC10"] == huc_number].copy()
        return study_basin

    # Filtering by hydrologic basin
    def spatial_filter_by_study_area(self, sites):
        study_polygon = self.get_study_polygon()
        # filter rain and well sites by study basin
        sites = sites.spatial.select(study_polygon).copy()
        return sites

    def download_data(
        self,
        date_start,
        date_end,
        location_query_params,
        param_cd,
        filter_by_study_area=True
    ):
        # Get ids based on query params
        locations = self.get_location_information(location_query_params)

        # Filter by study area polygon
        if filter_by_study_area:
            locations = self.spatial_filter_by_study_area(locations)
        site_ids = locations["site_id"].unique()

        # Retrieve data
        sites_dfs = []
        for site_id in site_ids:
            df = self.get_site_data(site_id, date_start, date_end, param_cd)
            sites_dfs.append(df)

        # Concat data
        site_data = pd.concat(sites_dfs)

        # arcgis needs coords to be numberic
        site_data["latitude"] = pd.to_numeric(site_data["latitude"])
        site_data["longitude"] = pd.to_numeric(site_data["longitude"])

        # Convert to sdf
        site_data = pd.DataFrame.spatial.from_xy(
            df=site_data,
            x_column="longitude",
            y_column="latitude",
        )

        # Merge site info with timeseries info...
        site_data = site_data.merge(
            locations.loc[:, ["site_id", "altitude", "altidude_datum_code"]],
            how="left",
            left_on="site_id",
            right_on="site_id"
        )

        return site_data

    def download_rain_data(
        self,
        date_start,
        date_end,
        location_query_params=rain_query_params,
        param_cd=rain_cd,
        filter_by_study_area=True,
        output_csv=None
    ):
        data = self.download_data(
            date_start,
            date_end,
            location_query_params,
            param_cd,
            filter_by_study_area
        )

        if output_csv:
            data.to_csv(output_csv, index=False)
            print(f"Data saved to:{output_csv}")

        return data

    def download_well_data(
        self,
        date_start,
        date_end,
        location_query_params=well_query_params,
        param_cd=gw_depth_cd,
        filter_by_study_area=True,
        output_csv=None
    ):
        data = self.download_data(
            date_start,
            date_end,
            location_query_params,
            param_cd,
            filter_by_study_area
        )

        if output_csv:
            data.to_csv(output_csv, index=False)
            print(f"Data saved to:{output_csv}")

        return data


def download_study_data():
    print("Downloading study data...")
    usgs_study_data = UsgsStudyData()
    date_start = "2000-01-01"
    date_end = "2019-01-31"

    usgs_study_data.download_rain_data(
        date_start,
        date_end,
        filter_by_study_area=True,
        output_csv=usgs_rain_csv
    )
    usgs_study_data.download_well_data(
        date_start,
        date_end,
        filter_by_study_area=True,
        output_csv=usgs_well_csv
    )
    print("Done...")


if __name__ == "__main__":
    download_study_data()
