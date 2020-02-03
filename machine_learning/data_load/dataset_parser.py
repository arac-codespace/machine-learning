import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path
import pdb


# Relate original dataset column names to database tables.
SITE_COLS = {
    "site_id": [
        "site_no", "StationCode"
    ],
    "site_name": [
        "station_nm", "StationName"
    ],
    "latitude": [
        "dec_lat_va", "Latitude"
    ],
    "longitude": [
        "dec_long_va", "Longitude"
    ],
    "location": [
        "county_cd", "ReserveName"
    ], 
    "description": [
        "ParametersReported"
    ],
    "site_type": [
        "StationType"
    ],            
    "source": [
        "agency_cd"
    ],
    "datum": [
        "dec_coord_datum_cd"
    ],
    "vertical_datum": [
        "alt_datum_cd"
    ],
    "gage_altitude": [
        "alt_va"
    ],
    "hydrologic_unit": [
        "huc_cd"
    ],
    "local_aquifer": [
        "aqfr_cd"
    ],
    "aquifer_type": [
        "aqfr_type_cd"
    ],    
    "well_depth": [
        "well_depth_va"
    ],
    "hole_depth": [
        "hole_depth_va"
    ]
}

WELL_DATA_COLS = {
    "source": [
        "agency_cd"
    ],
    "site_id": [
        "site_no"
    ],
    "date_time": [
        "datetime"
    ],
    "timezone": [
        "tz_cd"
    ],
    "review_stage": [
        "165603_72019_cd"
    ],    
    "water_level_depth": [
        "165603_72019"
    ]
}

WATER_QUALITY_COLS = {
    "site_id": [
        "StationCode"
    ],
    "date_time": [
        "DateTimeStamp"
    ],
    "review_stage": [
        "Historical"
    ],
    "temperature": [
        "Temp"
    ],
    "temperature_flag": [
        "F_Temp"
    ],
    "specific_conductivity": [
        "SpCond"
    ],
    "specific_conductivity_flag": [
        "F_SpCond"
    ],
    "salinity": [
        "Sal"
    ],
    "salinity_flag": [
        "F_Sal"
    ],    
    "dissolved_oxygen_percent": [
        "DO_Pct"
    ],
    "dissolved_oxygen_percent_flag": [
        "F_DO_Pct"
    ],    
    "dissolved_oxygen": [
        "DO_mgl"
    ],
    "dissolved_oxygen_flag": [
        "F_DO_mgl"
    ],    
    "depth": [
        "Depth"
    ],
    "depth_flag": [
        "F_Depth"
    ],    
    "pH": [
        "pH"
    ],
    "pH_flag": [
        "F_pH"
    ],    
    "turbidity": [
        "Turb"
    ],
    "turbidity_flag": [
        "F_Turb"
    ],    
    "chlorophyll_fluorescence": [
        "ChlFluor"
    ],
    "chlorophyll_fluorescence_flag": [
        "F_ChlFluor"
    ]    
}


WATER_NUTRIENTS_COLS = {
    "site_id": [
        "StationCode"
    ],
    "date_time": [
        "DateTimeStamp"
    ],
    "review_stage": [
        "Historical"
    ],
    "orthophosphate": [
        "PO4F"
    ],
    "orthophosphate_flag": [
        "F_PO4F"
    ],
    "ammonium": [
        "NH4F"
    ],
    "ammonium_flag": [
        "F_NH4F"
    ],
    "nitrite": [
        "NO2F"
    ],
    "nitrite_flag": [
        "F_NO2F"
    ],
    "nitrate": [
        "NO3F"
    ],
    "nitrate_flag": [
        "F_NO3F"
    ],
    "nitrite_nitrate": [
        "NO23F"
    ],
    "nitrite_nitrate_flag": [
        "F_NO23F"
    ],
    "chlorophyll": [
        "CHLA_N"
    ],
    "chlorophyll_flag": [
        "F_CHLA_N"
    ]
}

PRECIPITATION_COLS = {
    "site_id": [
        "StationCode"
    ],
    "date_time": [
        "DateTimeStamp", "DatetimeStamp"
    ],
    "review_stage": [
        "Historical"
    ],
    "atmospheric_temperature":[
        "ATemp"
    ],
    "atmospheric_temperature_flag":[
        "F_ATemp"
    ],
    "relative_humidity":[
        "RH"
    ],
    "relative_humidity_flag":[
        "F_RH"
    ],
    "barometric_pressure":[
        "BP"
    ],
    "barometric_pressure_flag":[
        "F_BP"
    ],
    "wind_speed":[
        "WSpd"
    ],
    "wind_speed_flag":[
        "F_WSpd"
    ],
    "total_PAR":[
        "TotPAR"
    ],
    "total_PAR_flag":[
        "F_TotPAR"
    ],
    "total_precipitation":[
        "TotPrcp"
    ],
    "total_precipitation_flag":[
        "F_TotPrcp"
    ],
    "total_solar_radiation":[
        "TotSoRad"
    ],
    "total_solar_radiation_flag":[
        "F_TotSoRad"
    ],
}

# NERR station type codes...
NERR_STATION_TYPE = {
    0: "Meteorological",
    1: "Water Quality",
    2: "Nutrient",
}

# USGS County codes
COUNTY_CODES = {
    57: "Guayama",
    59: "Guayanilla",
    75: "Juana Díaz",
    111: "Peñuelas",
    113: "Ponce",
    121: "Sabana Grande",
    123: "Salinas",
    133: "Santa Isabel",
}


class DataParser():

    # Function that maps parsing functions with table names...
    def get_parser(self, tablename):
        table_parser = {
            "site": self.parse_site_data,
            "well_data": self.parse_well_data,
            "water_quality_data": self.parse_water_quality_data,
            "water_nutrient_data": self.parse_water_nutrient_data,
            "precipitation_data": self.parse_precipitation_data
        }

        parser = table_parser.get(tablename, None)

        if None:
            raise "Parsing of input data not currently supported..."
        else:
            return parser

    # Function to rename columns to database column names given an argument and a dictionary...
    def rename_columns(self, argument, table_cols):
        # if argument is inside the values of the dictionary, iterate and get the key...
        is_in_dict = argument in [x for v in table_cols.values() for x in v]
        if is_in_dict:
            # Iterate through keys, get value list and return key if argument
            for key in table_cols.keys():
                # Get values associated to db columns...
                column_values = table_cols.get(key)
                if column_values and argument in column_values:
                    return key
        else:
            return "to_drop"

    # Parser for the SITE database table...
    # Parses original csv datasets so it conforms with the SQL database schema.
    def parse_site_data(self, df, source):
        if source == "USGS":
            # Replace county codes with names...
            if "county_cd" in df.columns:
                df["county_cd"] = df["county_cd"].apply(
                    lambda x: COUNTY_CODES.get(x))
            # Rename columns...
            df = df.rename(columns=lambda col: self.rename_columns(col, SITE_COLS))
            # Add and Inquire about site type?
            df["site_type"] = "Groundwater Well"
            # Drop irrelevant columns...
            if "to_drop" in df.columns:
                df = df.drop('to_drop', axis='columns')
            # Add columns that are in the database but that aren't part of the original dataset
            for key in SITE_COLS:
                if key not in df.columns:
                    df[key] = None            
            return df

        elif source == "NERR":
            # Rename columns...
            df = df.rename(columns=lambda col: self.rename_columns(col, SITE_COLS))        
            # Replace station type with strings...
            if "site_type" in df.columns:
                df["site_type"] = df["site_type"].apply(
                    lambda x: NERR_STATION_TYPE.get(x)
                )        
            # Drop irrelevant columns...
            if "to_drop" in df.columns:
                df = df.drop('to_drop', axis='columns')
            # Add missing source
            df["source"] = source
            # Add columns that are in the database but that aren't part of the original dataset
            for key in SITE_COLS:
                if key not in df.columns:
                    df[key] = None
            # Filter the dataframe so it returns only the rows of interest...
            df = df.loc[df["location"] == "Jobos Bay"]        
            return df
        else:
            raise "Parsing for current file and/or source is not supported..."

    # Parser for the well_data database table...
    # Parses original csv datasets so it conforms with the SQL database schema.
    def parse_well_data(self, df, source):
        if source == "USGS":
            # Rename columns...
            df = df.rename(columns=lambda col: self.rename_columns(col, WELL_DATA_COLS))
            # Drop irrelevant columns...
            if "to_drop" in df.columns:
                df = df.drop('to_drop', axis='columns')        
            # Use date_time to set non datetime vals from the original tsv into NaT
            # That way it's possible to drop rows that don't have real data...        
            df["date_time"] = pd.to_datetime(df["date_time"], errors="coerce")
            df = df.dropna(subset=['date_time'])
            # Add columns that are in the database but that aren't part of the original dataset
            for key in WELL_DATA_COLS:
                if key not in df.columns:
                    df[key] = None
        # Replace review_stage code with strings...
            if "review_stage" in df.columns:
                # USGS quality control codes...
                REVIEW_STAGE_CODES = {
                    "P": "Provisional",
                    "A": "Authenticated"
                }            
                df["review_stage"] = df["review_stage"].apply(
                    lambda x: REVIEW_STAGE_CODES.get(x)
                )                  
            return df
        else:
            raise "Parsing for current file and/or source is not supported..."


    def parse_water_quality_data(self, df, source):
        if source == "NERR":

            # Change the review_stage column from codes to strings...
            def set_review_stage(row):
                if row["Historical"] == 1:
                    return "Authenticated"
                elif row["ProvisionalPlus"] == 1:
                    return "ProvisionalPlus"
                else:
                    return "Provisional"

            df["Historical"] = df.apply(lambda row: set_review_stage(row), axis=1)
            # Rename columns...
            df = df.rename(columns=lambda col: self.rename_columns(col, WATER_QUALITY_COLS))
            # Drop irrelevant columns...
            if "to_drop" in df.columns:
                df = df.drop('to_drop', axis='columns')        
            # Use date_time to set non datetime vals from the original tsv into NaT
            # That way it's possible to drop rows that don't have real data...        
            df["date_time"] = pd.to_datetime(df["date_time"], errors="coerce")
            df = df.dropna(subset=['date_time'])
            # Add columns that are in the database but that aren't part of the original dataset
            for key in WATER_QUALITY_COLS:
                if key not in df.columns:
                    df[key] = None
            # Add missing source
            df["source"] = source
            df["timezone"] = "LST"                              
            return df
        else:
            raise "Parsing for current file and/or source is not supported..."


    def parse_water_nutrient_data(self, df, source):
        if source == "NERR":
            # Change the review_stage column from codes to strings...
            def set_review_stage(row):
                if row["Historical"] == 1:
                    return "Authenticated"
                elif row["ProvisionalPlus"] == 1:
                    return "ProvisionalPlus"
                else:
                    return "Provisional"

            df["Historical"] = df.apply(lambda row: set_review_stage(row), axis=1)
            # Rename columns...
            df = df.rename(columns=lambda col: self.rename_columns(col, WATER_NUTRIENTS_COLS))
            # Drop irrelevant columns...
            if "to_drop" in df.columns:
                df = df.drop('to_drop', axis='columns')        
            # Use date_time to set non datetime vals from the original tsv into NaT
            # That way it's possible to drop rows that don't have real data...        
            df["date_time"] = pd.to_datetime(df["date_time"], errors="coerce")
            df = df.dropna(subset=['date_time'])
            # Add columns that are in the database but that aren't part of the original dataset
            for key in WATER_NUTRIENTS_COLS:
                if key not in df.columns:
                    df[key] = None
            # Add missing source
            df["source"] = source
            df["timezone"] = "LST"                             
            return df
        else:
            raise "Parsing for current file and/or source is not supported..."


    def parse_precipitation_data(self, df, source):
        if source == "NERR":
            # Change the review_stage column from codes to strings...
            def set_review_stage(row):
                if row["Historical"] == 1:
                    return "Authenticated"
                elif row["ProvisionalPlus"] == 1:
                    return "ProvisionalPlus"
                else:
                    return "Provisional"

            df["Historical"] = df.apply(lambda row: set_review_stage(row), axis=1)
            # Rename columns...
            df = df.rename(columns=lambda col: self.rename_columns(col, PRECIPITATION_COLS))
            # Drop irrelevant columns...
            if "to_drop" in df.columns:
                df = df.drop('to_drop', axis='columns')
            # Use date_time to set non datetime vals from the original tsv into NaT
            # That way it's possible to drop rows that don't have real data...        
            df["date_time"] = pd.to_datetime(df["date_time"], errors="coerce")
            df = df.dropna(subset=['date_time'])
            # Add columns that are in the database but that aren't part of the original dataset
            for key in PRECIPITATION_COLS:
                if key not in df.columns:
                    df[key] = None
            # Add missing source
            df["source"] = source
            df["timezone"] = "LST"
            return df
        else:
            raise "Parsing for current file and/or source is not supported..."
