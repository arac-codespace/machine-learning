# Machine Learning and Water Data

This is a repository for exploring the applications of machine learning techniques in the water sciences.

# Changelog

## [TODO]
- Start the data exploration branch.
- Current seed method is way too slow.  May want to move away from pandas and
  use pyodbc with an SQL statement to avoid duplicates (With CTE).
- I may want to change the data repository to sqlite or some shareable type of storage.

## [0.0.01] - 2020-03-30
### Notes
- IMPORTANT:  You must change the get observations usgs function to allow querying for multiple sites using the 'sites' kwarg which the USGS API is able to take!


## [0.0.01] - 2020-03-29
### Notes
- I've decided to switch from using a local SQL Database to using the USGS Instantaneous Values Web Service and focus solely on groundwater data for now.  This will also allow me the flexibility to explore other areas of interest without the hassle of having to maintain a database.  It should also make it easier to share code.

- I've also decided to use a combination of Plotly for Jupyter Lab prototyping and Dash for sharing in the future.  We'll see how this goes.

- Another thing.  Making Jupyterlab work with the arcgis api (and ipywidgets) is a pain if you're trying to use the latest version as of today (2.0.1).  Stick with 1.2.6 and make sure you've installed ipywidgets, arcgis, the jupyter extension manager and the jupyter arcgis-map-ipywidget extension.


## [0.0.01] - 2020-02-22
### Notes
- [IMPORTANT] The sampling_sites.csv is missing the negative number for the longitude of the Jobos Bay sites.  I've updated the SQL database to fix this issue.
- The arcgis API doesn't like Nan, therefore it's important to replace those values with None or some other appropiate value when mapping...

### Added
- Created the classes to handle data fetching.

## [0.0.01] - 2020-02-16
### Notes
- Generated the machine_learning_pr database schema script.
- Seeded the database after creating the proper schema so as to assure that the
  data is of the proper data type.

### Changed
- Refactored a lot of stuff in the dataset_parser.py.

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

# Resources
### Random web resources:
- https://www.machinelearningplus.com/time-series/time-series-analysis-python/
- https://towardsdatascience.com/an-end-to-end-project-on-time-series-analysis-and-forecasting-with-python-4835e6bf050b
- https://www.analyticsvidhya.com/blog/2016/02/time-series-forecasting-codes-python/

### Primary sources (see study resources):
- A Comparative Study of Groundwater Level Forecasting Using Data-Driven Models Based on Ensemble Empirical Mode Decomposition (Nice method section!)
- Short‑term prediction of groundwater level using improved random forest regression with a combination of random features
- Understanding groundwater table using a statistical model (interesting...)