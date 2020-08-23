from app_constants import (
    raw_nerr_data_path,
    nerr_wq_data_path,
    nerr_met_data_path,
    nerr_nut_data_path,
    nerr_stations_data_path
)

import pandas as pd


wq_cols = [
    "StationCode",
    #     "isSWMP",
    "DateTimeStamp",
    "Historical",
    "ProvisionalPlus",
    #     "F_Record",
    "Temp",
    "F_Temp",
    "SpCond",
    "F_SpCond",
    "Sal",
    "F_Sal",
    "DO_Pct",
    "F_DO_Pct",
    "DO_mgl",
    "F_DO_mgl",
    "Depth",
    "F_Depth",
    "cDepth",
    "F_cDepth",
    #     "Level",
    #     "F_Level",
    #     "cLevel",
    #     "F_cLevel",
    "pH",
    "F_pH",
    "Turb",
    "F_Turb",
    "ChlFluor",
    "F_ChlFluor"
]

met_cols = [
    'StationCode',
    # 'isSWMP',
    'DatetimeStamp',
    'Historical',
    'ProvisionalPlus',
    'Frequency',
    #     'F_Record',
    'ATemp',
    'F_ATemp',
    'RH',
    'F_RH',
    'BP',
    'F_BP',
    'WSpd',
    'F_WSpd',
    'MaxWSpd',
    'F_MaxWSpd',
    'MaxWSpdT',
    'Wdir',
    'F_Wdir',
    'SDWDir',
    'F_SDWDir',
    'TotPAR',
    'F_TotPAR',
    'TotPrcp',
    'F_TotPrcp',
    #     'TotSoRad',
    #     'F_TotSoRad',
]

nut_cols = [
    'StationCode',
    # 'isSWMP',
    'DateTimeStamp',
    'Historical',
    'ProvisionalPlus',
    #     'CollMethd',
    #     'REP',
    #     'F_Record',
    'PO4F',
    'F_PO4F',
    'NH4F',
    'F_NH4F',
    'NO2F',
    'F_NO2F',
    'NO3F',
    'F_NO3F',
    'NO23F',
    'F_NO23F',
    'CHLA_N',
    'F_CHLA_N',
]

# NOTE: Some of the columns have spaces in the source...
station_cols = [
    #     'Row',
    #     'NERR Site ID ',
    'Station Code',
    'Station Name',
    #     'Lat Long',
    'Latitude ',
    ' Longitude',
    ' Status',
    ' Active Dates',
    ' State',
    ' Reserve Name',
    #     'Real Time',
    #     'HADS ID',
    'GMT Offset',
    #     'Station Type',
    #     'Region',
    #     'isSWMP',
    #     'Parameters Reported'
]

# Iterate through directory files and filter by extension
# and a sequence of characters in the filename
def get_fnames_by_dataset(dirr, fname_filter, ext):
    fnames = [
        e for e in dirr.iterdir() if e.suffix == ext and fname_filter in e.stem
    ]
    return fnames


# Get filenames from directory filtered by nerr dataset
# and merge files into a dataframe
def merge_files_by_dataset(
    dirr,
    fname_filter,
    ext,
    usecols,
    encoding="utf-8"
):
    files = get_fnames_by_dataset(dirr, fname_filter, ext)
    df = pd.concat(
        (pd.read_csv(f, usecols=usecols, encoding=encoding) for f in files)
    )
    return df


# Some string columns have right whitespace.
# This fx selects all objects dtype columns
# strips whitespace from all of those columns.
def strip_whitespace(df):
    df_obj = df.select_dtypes(include=['object'])
    df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
    df.StationCode.unique()
    return df

# Merge wq files from dirr and
# return df
def merge_wq_files(dirr):
    usecols = wq_cols
    fname_filter = "wq"
    ext = ".csv"
    df = merge_files_by_dataset(dirr, fname_filter, ext, usecols)
    df.columns = df.columns.str.replace(' ', '')
    df = strip_whitespace(df)
    return df


# Merge met files from dirr and
# return df
def merge_met_files(dirr):
    usecols = met_cols
    fname_filter = "met"
    ext = ".csv"
    df = merge_files_by_dataset(dirr, fname_filter, ext, usecols)
    df = df.rename(columns={"DatetimeStamp": "DateTimeStamp"})
    df.columns = df.columns.str.replace(' ', '')
    df = strip_whitespace(df)
    return df


# Merge nut files from dirr and
# return df
def merge_nut_files(dirr):
    usecols = nut_cols
    fname_filter = "nut"
    ext = ".csv"
    df = merge_files_by_dataset(dirr, fname_filter, ext, usecols)
    df.columns = df.columns.str.replace(' ', '')
    df = strip_whitespace(df)
    return df


# Merge stations files from dirr and
# return df
def merge_stations_files(dirr):
    usecols = station_cols
    fname_filter = "sampling"
    ext = ".csv"
    df = merge_files_by_dataset(
        dirr, fname_filter, ext, usecols, encoding="latin")
    df.columns = df.columns.str.replace(' ', '')
    df = strip_whitespace(df)
    return df

if __name__ == "__main__":

    # Save to output
    wq_df = merge_wq_files(raw_nerr_data_path)
    wq_df.to_csv(nerr_wq_data_path, index=False)

    met_df = merge_met_files(raw_nerr_data_path)
    met_df.to_csv(nerr_met_data_path, index=False)

    nut_df = merge_nut_files(raw_nerr_data_path)
    nut_df.to_csv(nerr_nut_data_path, index=False)

    stations_df = merge_stations_files(raw_nerr_data_path)
    stations_df.to_csv(nerr_stations_data_path, index=False)
