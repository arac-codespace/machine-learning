from data_load.helpers import get_engine
import pandas as pd
from datetime import datetime
import pdb

class Station():
    def __init__(self):
        self.id = None
        self.source = None
        self.start = None
        self.end = None
        self._queried_observation_data = None
        self._queried_location_data = None

    # Fetch data from sql server...
    def _fetch_data(self):
        # Get stored params...
        id = self.id
        start = self.start
        end = self.end
        source = self.source

        # Get engine...
        engine = get_engine()
        tablename = "well_data"
        
        # load database records
        print("Loading database records...")
        sql_query = """
            SELECT *
            FROM {tablename}
            WHERE station_id = '{id}'
            AND date_time BETWEEN '{start}' AND '{end}'
            AND source = '{source}';
        """.format(id = id, start = start, end = end, source = source, tablename=tablename)

        df = pd.read_sql(sql_query, con=engine)
        df = self._parse_data(df)        
        return df

    def _fetch_location_data(self):
        # Get stored params...
        id = self.id

        # Get engine...
        engine = get_engine()
        tablename = "usgs_station"
        
        # load database records
        print("Loading database records...")
        sql_query = """
            SELECT *
            FROM {tablename}
            WHERE station_id = '{id}';
        """.format(id = id, tablename=tablename)

        df = pd.read_sql(sql_query, con=engine)
        return df      

    # Modify fetched data...
    def _parse_data(self, df):
        df["date_time"] = pd.to_datetime(df["date_time"])
        return df

    # Data loader...
    def find_data(self, id, start, end, source= "USGS"):
        # If id's different, get location data...
        if self.id != id:
            self.id = id
            df = self._fetch_location_data()
            self._queried_location_data = df

        # Compares provided params to avoid unnecessary sql fetching...
        if (self.start, self.end, self.source) != (start, end, source):
            # Set params...
            self.start = start
            self.end = end
            self.source = source            
            # Fetches data from database based on new params...
            df = self._fetch_data()
            # Set data...
            self._queried_observation_data = df
            return self
        else:
            return self

    # Well data getter...
    def get_observation_data(self):
        df = self._queried_observation_data
        return df

    # Location data getter...
    def get_location_data(self):
        df = self._queried_location_data
        return df
    # Location - well data getter...
    def get_data(self):
        df1 = self.get_observation_data()
        df2 = self.get_location_data()
        df_join = pd.merge(df1, df2, on = "station_id", how = "left")
        return df_join



# class Stations():
#     def __init__(self):
#         self.cards = []

if __name__ == '__main__':
    id = "175711066143600"
    start = datetime(1950, 1, 1).replace(microsecond=0)
    end = datetime.now().replace(microsecond=0)
    source= "USGS"
    station = Station().find_data(id, start, end, source)
    df = station.get_data()
    print(df)