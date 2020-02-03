import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path
from helpers import get_engine
import pdb
from dataset_parser import DataParser


# load csv and parse...
def load_csv(file_path, tablename, source):
    print("Parsing csv...")
    df = pd.read_csv(file_path, encoding="ISO-8859-1",
                     dtype={'site_no': object})
    df.columns = df.columns.str.replace(' ', '')

    # Select all string values and strip whitespace...
    df_obj = df.select_dtypes(['object'])
    df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())

    # Do dataframe operations according to table name provided
    parsed_df = DataParser().get_parser(tablename)(df, source)

    return parsed_df


def populate_data(df, tablename, subset, update_db=False):
    # Get engine...
    engine = get_engine()

    # load database records
    print("Loading database records to drop duplicates...")
    sql_query = """
		SELECT *
		FROM {tablename}
	""".format(tablename=tablename)
    try:
        df2 = pd.read_sql(sql_query, con=engine)
        if "date_time" in df2.columns:
            df2["date_time"] = pd.to_datetime(df2["date_time"])

        # compare records and drop duplicates...
        print("Dropping duplicates...")
        unique_df = pd.concat([df, df2]).drop_duplicates(
            subset=subset, keep=False).reset_index(drop=True)
        # If there are non-duplicated records...
        if update_db and not unique_df.empty:
            print("New records found.  Inserting into database...")
            unique_df.to_sql(tablename, con=engine,
                            if_exists="append", index=False)
        else:
            print("No new records found...")
            print(df)            
    except Exception as err:
        # If table doesn't exist, set update db to original df...
        print(err)
        df.to_sql(tablename, con=engine,
                        if_exists="append", index=False)


def insert_sampling_sites(tablename = "site", update_db = False):
    # Create path to file...
    current_path = Path()
    file_path = current_path/"raw_data\\USGS_Wells\\usgs_sampling_stations.csv"
    file_path = str(file_path.absolute())

    # load parsed df
    df1 = load_csv(file_path, tablename, "USGS")


    file_path = current_path/"raw_data\\NERR\\nerr_data_12-14-2019\\sampling_stations.csv"
    file_path = str(file_path.absolute())

    # load parsed df
    df2 = load_csv(file_path, tablename, "NERR")
 
    df = pd.concat([df1,df2]).reset_index(drop=True)
    subset = "site_id"

    if update_db:        
        populate_data(df, tablename, subset, update_db=False)
    else:
        # Save concat file...
        current_path = Path()
        file_path = current_path/"raw_data\\{tablename}.csv".format(tablename=tablename)
        df.to_csv(file_path.absolute(), index=False)        
        return df

def insert_nerr_data(tablename, update_db = False):
    NERR_TABLENAME_TO_FILE = {
        "water_quality_data": "wq",
        "water_nutrient_data": "nut",
        "precipitation_data": "met"
    }
    source = "NERR"

    # Create path to directory...
    current_path = Path()
    file_path = current_path/"raw_data\\NERR\\nerr_data_12-14-2019\\"
    file_path = file_path.absolute()
    
    # Iterate through files...
    files = file_path.absolute().glob("*.csv")
    df_list = []    
    for f in files:
        if NERR_TABLENAME_TO_FILE.get(tablename) in f.name:
            print(f.name)
            df_list.append(load_csv(f, tablename, source))
    df = pd.concat(df_list, ignore_index=True)

    subset = ["site_id", "source", "date_time"]
    if update_db:        
        populate_data(df, tablename, subset, update_db=False)
    else:
        # Save concat file...
        current_path = Path()
        file_path = current_path/"raw_data\\{tablename}.csv".format(tablename=tablename)
        df.to_csv(file_path.absolute(), index=False)          
        return df

def insert_usgs_data(tablename, update_db = False):
    # Create path to directory...
    current_path = Path()
    file_path = current_path/"raw_data\\USGS_Wells\\well_data_south_aquifer_12-29-2019.csv"
    file_path = file_path.absolute()
    source = "USGS"
 
    df = load_csv(file_path, tablename, source)

    subset = ["site_id", "source", "date_time"]
    if update_db:        
        populate_data(df, tablename, subset, update_db=False)
    else:
        # Save concat file...
        current_path = Path()
        file_path = current_path/"raw_data\\{tablename}.csv".format(tablename=tablename)
        df.to_csv(file_path.absolute(), index=False)          
        return df


if __name__ == '__main__':
    insert_sampling_sites(update_db = False)
    insert_nerr_data("water_quality_data", update_db = False)
    insert_nerr_data("water_nutrient_data", update_db = False)
    insert_nerr_data("precipitation_data", update_db = False)     
    insert_usgs_data("well_data", update_db = False)