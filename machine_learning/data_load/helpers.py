from datetime import datetime
from sqlalchemy import create_engine

def tz_aware(dt):
    return dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None

# Create the engine to connect to the database...
def get_engine():
    server = r"DESKTOP-4IL536V\SQLEXPRESS"
    database = "pr_timeseries"
    print("Creating engine for {database} at {server}".format(database=database, server=server))

    engine = create_engine(
        'mssql+pyodbc://@' + server + '/' + database +
        '?trusted_connection=yes&driver=ODBC+Driver+13+for+SQL+Server'
    )
    return engine