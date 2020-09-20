import pandas as pd
from preprocess_data.data_paths import (
    raw_nerr_data_path,
    nerr_wq_data_path,
    nerr_met_data_path,
    nerr_nut_data_path,
    nerr_stations_data_path
)
from preprocess_data.data_constants import (
    wq_cols,
    met_cols,
    nut_cols,
    station_cols
)


def without_keys(d, invalid):
    new_dtypes = {x: d[x] for x in d if x not in invalid}
    return new_dtypes


def exclude_datetime_cols(dtypes_dict):
    invalid = ["DateTimeStamp", "DatetimeStamp"]
    return without_keys(dtypes_dict, invalid)


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
    dtypes,
    encoding="utf-8"
):
    files = get_fnames_by_dataset(dirr, fname_filter, ext)
    df = pd.concat(
        (pd.read_csv(f, usecols=usecols, encoding=encoding, dtype=dtypes, parse_dates=True) for f in files)
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


# Separates comment codes from numeric quality codes
# that resides in the F_* columns
def convert_flags_to_numeric_code(df):
    # Replaces original column series
    # with an integer only series.
    # Used with the apply df function.
    def extract_flag_code(col):
        # One or more <, first group
        # May have 1 or no -, followed by
        # any number of digits and capped by
        # a > or a not numeric.
        regex = r"<?(-?\d+)>?\D?"
        integer_flags = col.str.extract(regex, expand=False)
        return integer_flags

    # Select all flag columns...
    flag_cols = df.filter(like='F_', axis=1).columns
    flag_cols_df = df.loc[:, flag_cols]
    # Need to convert columns dtypes to object because
    # In cases where the entire column is nan pandas
    # will assign a float dtype
    flag_cols_df = flag_cols_df.astype("O")
    # Replace non numeric values with numeric flag values
    flag_cols_df = flag_cols_df.apply(lambda x: extract_flag_code(x))
    # Convert to numeric
    # This should NOT return an error if the regex did its job well
    flag_cols_df = flag_cols_df.apply(lambda x: pd.to_numeric(x))
    df.loc[:, flag_cols] = flag_cols_df
    return df


# Merge wq files from dirr and
# return df
def merge_wq_files(dirr=raw_nerr_data_path):
    usecols = wq_cols.keys()
    dtypes = exclude_datetime_cols(wq_cols)
    fname_filter = "wq"
    ext = ".csv"
    df = merge_files_by_dataset(
        dirr,
        fname_filter,
        ext,
        usecols=usecols,
        dtypes=dtypes
    )
    df.columns = df.columns.str.replace(' ', '')
    df = strip_whitespace(df)
    df = convert_flags_to_numeric_code(df)
    return df


# Merge met files from dirr and
# return df
def merge_met_files(dirr=raw_nerr_data_path):
    usecols = met_cols.keys()
    dtypes = exclude_datetime_cols(met_cols)
    fname_filter = "met"
    ext = ".csv"
    df = merge_files_by_dataset(
        dirr,
        fname_filter,
        ext,
        usecols=usecols,
        dtypes=dtypes
    )
    df = df.rename(columns={"DatetimeStamp": "DateTimeStamp"})
    df.columns = df.columns.str.replace(' ', '')
    df = strip_whitespace(df)
    df = convert_flags_to_numeric_code(df)
    return df


# Merge nut files from dirr and
# return df
def merge_nut_files(dirr=raw_nerr_data_path):
    usecols = nut_cols.keys()
    dtypes = exclude_datetime_cols(nut_cols)
    fname_filter = "nut"
    ext = ".csv"
    df = merge_files_by_dataset(
        dirr,
        fname_filter,
        ext,
        usecols=usecols,
        dtypes=dtypes
    )
    df.columns = df.columns.str.replace(' ', '')
    df = strip_whitespace(df)
    df = convert_flags_to_numeric_code(df)
    return df


# Merge stations files from dirr and
# return df
def merge_stations_files(dirr=raw_nerr_data_path):
    usecols = station_cols.keys()
    dtypes = exclude_datetime_cols(station_cols)
    fname_filter = "sampling"
    ext = ".csv"
    df = merge_files_by_dataset(
        dirr,
        fname_filter,
        ext,
        usecols=usecols,
        dtypes=dtypes,
        encoding="latin"
    )
    df.columns = df.columns.str.replace(' ', '')
    df = strip_whitespace(df)
    df = convert_flags_to_numeric_code(df)
    return df


if __name__ == "__main__":

    wq_df = merge_wq_files()
    met_df = merge_met_files()
    nut_df = merge_nut_files()
    stations_df = merge_stations_files()

    print(wq_df, met_df, nut_df, stations_df)
    # Save to output
    # wq_df = merge_wq_files(raw_nerr_data_path)
    # wq_df.to_csv(nerr_wq_data_path, index=False)

    # met_df = merge_met_files(raw_nerr_data_path)
    # met_df.to_csv(nerr_met_data_path, index=False)

    # nut_df = merge_nut_files(raw_nerr_data_path)
    # nut_df.to_csv(nerr_nut_data_path, index=False)

    # stations_df = merge_stations_files(raw_nerr_data_path)
    # stations_df.to_csv(nerr_stations_data_path, index=False)
