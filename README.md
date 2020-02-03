# Machine Learning and Water Data

This is a repository for exploring the applications of machine learning techniques in the water sciences.

# Changelog

## [TODO]
- Verify the integrity of the data.
- Modify the SQL tables so they have proper relationships and constraints setup.
- Save the resulting SQL schema as a script, perhaps save a backup of the data too.
- Create classes for each of the table to facilitate access to stored data.
- Start the data exploration branch.

## [0.0.01] - 2020-02-02
### Notes
-  Seeded the SQL database.  I've noticed warnings about different dtypes being on the same column.
  I have to check if it's something related to random strings in the original CSVs or if it's
  something related to the parsing process (ie: site_id for USGS datasets are recognized as int, but
  site_id can be int or a varchar).
- Had some issues pushing raw data files to github.  Had to force push to master with the changed code
  and alter the data-wrangling branch...

### Added
- Added this changelog.
- Added functions in the seed_database.py module with options to save the parsed data
  locally or in the database. 

### Changed
- Changed the previously named data_wrangling script.  Now data parsing tasks are held in a DataParser class
  under the dataset_parser module.
- Renamed data_wrangling.py to seed_database.py

# Groundwater Data
## USGS Data
Current and historic data for well depth measurements was obtained through the nwis website.  All available data for Hydrologic Unit 21010004 (Southern Puerto Rico) was queried (from 1950 to 12-29-2019).

Link: https://nwis.waterdata.usgs.gov

# Water Quality Data
## Jobos Bay Dataset
All available data up to 12-14-2019 was requested from the National Estuarine Research Reserve System's website.

Link: http://cdmo.baruch.sc.edu/

# Data Parsing
Sampling sites and their corresponding observations were uploaded into a simple SQL Server database.  Sites and observations were related by their usgs station code (site_no) or their nerr site code (StationCode) under
a custom column named site_id.  Columns of interest were kept and column named were renamed for the sake of clarity.  The parsing code used is under data_load/dataset_parser.py.

# Timezones
Observations from the USGS and NERR dataset are in LST (AST for Puerto Rico).