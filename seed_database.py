from database_operations.database import create_db_engine
from database_operations.models import (
    Stations,
    WaterQuality,
    Nutrients,
    Weather
)
from preprocess_data.process_nerr_data import (
    merge_wq_files,
    merge_met_files,
    merge_nut_files,
    merge_stations_files
)


if __name__ == "__main__":
    # LEFT HERE!  SQL DB GOT LOCKED SO I HAVENT TESTED THIS SCRIPT...
    engine = create_db_engine()
    print("Merging wq files...")
    wq_df = merge_wq_files()
    print("Uploading to DB")
    wq_df.to_sql("water_quality", index=False, con=engine, if_exists="replace")

    print("Merging met files...")
    met_df = merge_met_files()
    print("Uploading to DB")
    met_df.to_sql("weather", index=False, con=engine, if_exists="replace")

    print("Merging nutrient files...")
    nut_df = merge_nut_files()
    print("Uploading to DB")
    nut_df.to_sql("nutrients", index=False, con=engine, if_exists="replace")

    print("Merging station files...")
    stations_df = merge_stations_files()
    print("Uploading to DB")
    stations_df.to_sql("stations", index=False, con=engine, if_exists="replace")
