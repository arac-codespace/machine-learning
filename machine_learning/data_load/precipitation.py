# https://www.ncdc.noaa.gov/data-access
# https://www.ncei.noaa.gov/support/access-search-service-api-user-documentation

import pandas as pd
import requests, pytz, urllib
from datetime import datetime
from dateutil.parser import parse
from .helpers import tz_aware

class Station():
    def __init__(self,stationid,start_date,end_date):
        self.stationid = stationid
        self.start_date = self.format_date(start_date) 
        self.end_date = self.format_date(end_date)
    
    def format_date(self,date):
        # Accept strings and convert to isoformat
        # Timezone must be included...
        if type(date) is str:
            date_object = datetime.fromisoformat(date)
            # If timezone not provided, assume it's utc...
            if not tz_aware(date_object):
                date_object = pytz.utc.localize(date_object)
                return date_object
        else:
            raise TypeError("ERROR: Date parameter must be a string.")


class NceiStation(Station):
    def __init__(self,stationid,start_date,end_date):
        super().__init__(stationid,start_date,end_date)

    def precipitation(self):
        # Creates the dictionary for proper pandas consumption
        def parse_records(records):
            # This is where you specify the columns of interest and their names
            data = {"DATE":[], "HourlyPrecipitation":[]}

            for record in records:
                # Note: NCEI API DATE is NOT in UTC.  It's in standard local time and
                # no adjustments are made for DST...

                if "HourlyPrecipitation" in record.keys():
                    timestamp = parse(record["DATE"])
                    precipitationLastHour = record["HourlyPrecipitation"]
                    # Sometimes there are more than one record in one hour.  This condition
                    # filters out readings that occur outside the xx:56 hour mark.
                    if timestamp.strftime("%M") == '56':
                        # pdb.set_trace()
                        # For some reason, the precipitation column may have stuff other than numbers...
                        # So to deal with the numbers...
                        if precipitationLastHour == 'T' or precipitationLastHour== 'M' or precipitationLastHour == None:
                            precipitationLastHour = 0
                        else:
                            # Create a new string with only digits...
                            precipitationLastHour = ''.join([i for i in precipitationLastHour if i != "s"])

                        data["DATE"].append(timestamp)
                        data["HourlyPrecipitation"].append(float(precipitationLastHour))                
            return data

        response = response
        data = parse_records(response)

        df = pd.DataFrame(data)
        # convert m to inches
        # df["HourlyPrecipitation"]*= 39.37007874 
        # Converting into datetime object for query purposes 
        df["DATE"] = pd.to_datetime(df["DATE"])  

        # Format and Set additional fields for PRASA DB...
        rename = {"HourlyPrecipitation":"Precipitation_in", "DATE": "Date_Time"}
        df = df.rename(columns=rename)
        df["Interval"] = "1-hour"
        df["Data_Flag"] = None
        df["Documentation"] = "Hourly rain data collected from the NCEI JSON API."
        df["RG_location"] = "TJSJ"
        df["RG_Location_ID"] = None               
        # Create a csv/excel file for daily NWS data?
        df["SourceFile"] = None
        df["MissingValue"] = 0
        df["QC_Flag"] = "Validated"
        df["UploadDate"] = datetime.utcnow()
        df["UploadName"] = "NCEI_API"
        
        return df

        
    def sum_precipitation(self):
        # Total precipitation reported in the last 72 hours. (Inches)
        precipitation = self.precipitation()
        sum_precipitation = precipitation["Precipitation_in"].sum()
        return sum_precipitation 