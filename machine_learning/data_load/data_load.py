from .helpers import get_engine
import pandas as pd

# class Site():
#     def __init__(self):
#         self.tablename = "site"
#         self._dataframe = self._fetch_data()

#     # Fetch data from database once...
#     def _fetch_data(self):
#         engine = get_engine()
#         tablename = self.tablename

#         sql_query = """
#             SELECT *
#             FROM {tablename}
# 	    """.format(tablename=tablename)

#         df = pd.read_sql(sql_query, con=engine)
#         return df

#     # Return site data...
#     def get_data(self):
#         df = self._dataframe.copy()
#         return df

# TEMPORARY STUFF MUST THINK HOW TO DO THIS>...
class Site():
    def __init__(self):
        self.site_id = None
        self.site_type = None

        # Constant location data
        self.site_name = None
        self.latitude = None
        self.longitude = None
        self.source = None
        self.datum = None
        self.vertical_datum = None
        self.gage_altitude = None
        self.hole_depth = None
        self.well_depth = None
        self.hydrologic_unit = None
        self.local_aquifer = None
        self.description = None

        self.start = None
        self.end = None
        self._queried_observation_data = None
        self._queried_location_data = None
        self._all_sites = self._fetch_all_sites()

    # Fetch all sites stored in the database at init...
    def _fetch_all_sites(self):
        engine = get_engine()
        tablename = "site"

        sql_query = f"SELECT * FROM {tablename}"

        df = pd.read_sql(sql_query, con=engine)
        return df 

    # Fetch data from sql server...
    def _fetch_observation_data(self):
        # Get stored params...
        site_id = self.site_id
        start = self.start
        end = self.end
        site_type = self.site_type

        # Get engine...
        engine = get_engine()

        def get_table_name(site_type):
            if site_type == "Groundwater Well":
                return "well_data"
            elif site_type == "Water Quality":
                return "water_quality_data"
            elif site_type == "Nutrient":
                return "water_nutrient_data"
            elif site_type == "Meteorological":
                return "precipitation_data"
            else:
                raise f"ERROR: No table related for site of type {site_type}"
    
        tablename = get_table_name(site_type)
        
        # load database records
        print("Loading database records...")
        sql_query = f"SELECT * FROM {tablename} "
        sql_query += f"WHERE site_id = '{site_id}' "  
        sql_query += f"AND date_time BETWEEN '{start}' AND '{end}' "

        df = pd.read_sql(sql_query, con=engine)
        df = self._parse_data(df)        
        return df

    def _fetch_location_data(self):
        # Get stored params...
        site_id = self.site_id

        # Get engine...
        engine = get_engine()
        tablename = "site"
        
        # load database records
        print("Loading database records...")
        sql_query = f"SELECT * FROM {tablename} "
        sql_query += f"WHERE site_id = '{site_id}'"
        
        df = pd.read_sql(sql_query, con=engine)
        return df      

    # Modify fetched data...
    def _parse_data(self, df):
        df["date_time"] = pd.to_datetime(df["date_time"])
        return df

    # Data loader...
    def find_data(self, site_id, start, end, site_type):
        # If id's different, get location data...
        if self.site_id != site_id:
            self.site_id = site_id
            df = self._fetch_location_data()

            # Set constants as class instance variables...
            self.site_name = df["site_name"].iloc[0]             
            self.latitude = df["latitude"].iloc[0]
            self.longitude = df["longitude"].iloc[0]
            self.source = df["source"].iloc[0]
            self.datum = df["datum"].iloc[0]
            self.vertical_datum = df["vertical_datum"].iloc[0]
            self.gage_altitude = df["gage_altitude"].iloc[0]
            self.hole_depth = df["hole_depth"].iloc[0]
            self.well_depth = df["well_depth"].iloc[0]
            self.hydrologic_unit = df["hydrologic_unit"].iloc[0]
            self.local_aquifer = df["local_aquifer"].iloc[0]
            self.description = df["description"].iloc[0]

            self._queried_location_data = df

        # Compares provided params to avoid unnecessary sql fetching...
        if (self.start, self.end, self.site_type) != (start, end, site_type):
            # Set params...
            self.start = start
            self.end = end
            self.site_type = site_type            
            # Fetches data from database based on new params...
            df = self._fetch_observation_data()
            # Set data...
            self._queried_observation_data = df
            return self
        else:
            return self

    # Well data getter...
    def get_observation_data(self):
        df = self._queried_observation_data.copy()
        return df

    # Location data getter...
    def get_location_data(self):
        df = self._queried_location_data.copy()
        return df

    # All sites data getter...
    def get_all_sites(self):
        df = self._all_sites.copy()
        return df 


# # class Stations():
# #     def __init__(self):
# #         self.cards = []

# if __name__ == '__main__':
#     id = "175711066143600"
#     start = datetime(1950, 1, 1).replace(microsecond=0)
#     end = datetime.now().replace(microsecond=0)
#     source= "USGS"
#     station = Station().find_data(id, start, end, source)
#     df = station.get_data()
#     print(df)