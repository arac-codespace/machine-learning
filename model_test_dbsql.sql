# Water quality parameters
Temp
F_Temp
SpCond
F_SpCond
Sal
F_Sal
DO_pct
F_DO_pct
DO_mgl
F_DO_mgl
Depth
F_Depth
cDepth
F_cDepth
Level
F_Level
cLevel
F_cLevel
pH
F_pH
Turb
F_Turb
ChlFluor
F_ChlFluor

# Weather parameters
ATemp
F_ATemp
RH
F_RH
BP
F_BP
WSpd
F_WSpd
MaxWSpd
F_MaxWSpd
MaxWSpdT
F_MaxWSpdT
Wdir
F_Wdir
SDWDir
F_SDWDir
TotPAR
F_TotPAR
TotPrcp
F_TotPrcp
CumPrcp
F_CumPrcp
TotSoRad
F_TotSoRad

# Nutrient/pigment parameters*
PO4F
F_PO4F
NH4F
F_NH4F
NO2F
F_NO2F
NO3F
F_NO3F
NO23F
F_NO23F
CHLA_N
F_CHLA_N

# QA Flags
-5: Outside high sensor range
-4: Outside low sensor range
-3: Data rejected due to QA/QC
-2: Missing data
-1: Optional parameter not collected
0:  Passed initial QAQC checks
1:  Suspect data
2:  Reserved for future use*
3:  Calculated data: non-vented depth/level sensor correction for changes in barometric pressure*
4:  Historical: Pre-auto QA/QC
5:  Corrected data

# Station parameters
StationCode
StationName
Latitude
Longitude
Status
ActiveDates
State
ReserveName
HADSID
GMTOffset
StationType
Region


# //// -- LEVEL 1
# //// -- Tables and References
Table Stations {
  id int [pk, increment]
  StationCode varchar
  StationName varchar
  Latitude decimal
  Longitude decimal
  Status varchar
  ActiveDates varchar
  State varchar
  ReserveName varchar
  HADSID varchar
  GMTOffset varchar
  StationType varchar
  Region varchar
}

Table Nutrients {
  id int [pk, increment]
  StationCode int [ref: > Stations.id]
  DateTime timestamp
  PO4F decimal
  F_PO4F int [ref: > DataFlags.id]
  NH4F decimal 
  F_NH4F int [ref: > DataFlags.id]
  NO2F decimal
  F_NO2F int [ref: > DataFlags.id]
  NO3F decimal
  F_NO3F int [ref: > DataFlags.id]
  NO23F decimal
  F_NO23F int [ref: > DataFlags.id]
  CHLA_N decimal
  F_CHLA_N int [ref: > DataFlags.id]  
}

Table Weather {
  id int [pk, increment]
  StationCode int [ref: > Stations.id]
  DateTime timestamp
  ATemp decimal
  F_ATemp int [ref: > DataFlags.id]
  RH decimal
  F_RH int [ref: > DataFlags.id]
  BP decimal
  F_BP int [ref: > DataFlags.id]
  WSpd decimal
  F_WSpd int [ref: > DataFlags.id]
  MaxWSpd decimal
  F_MaxWSpd int [ref: > DataFlags.id]
  MaxWSpdT decimal
  F_MaxWSpdT int [ref: > DataFlags.id]
  Wdir decimal
  F_Wdir int [ref: > DataFlags.id]
  SDWDir decimal
  F_SDWDir int [ref: > DataFlags.id]
  TotPAR decimal
  F_TotPAR int [ref: > DataFlags.id]
  TotPrcp decimal
  F_TotPrcp int [ref: > DataFlags.id]
  CumPrcp decimal
  F_CumPrcp int [ref: > DataFlags.id]
  TotSoRad decimal
  F_TotSoRad int [ref: > DataFlags.id]  
}

Table WaterQuality {
  id int [pk, increment]
  StationCode int [ref: > Stations.id]
  DateTime timestamp
  Temp decimal
  F_Temp int [ref: > DataFlags.id] 
  SpCond decimal
  F_SpCond int [ref: > DataFlags.id] 
  Sal decimal
  F_Sal int [ref: > DataFlags.id] 
  DO_pct decimal
  F_DO_pct int [ref: > DataFlags.id] 
  DO_mgl decimal
  F_DO_mgl int [ref: > DataFlags.id] 
  Depth decimal
  F_Depth int [ref: > DataFlags.id] 
  cDepth decimal
  F_cDepth int [ref: > DataFlags.id] 
  Level decimal
  F_Level int [ref: > DataFlags.id] 
  cLevel decimal
  F_cLevel int [ref: > DataFlags.id] 
  pH decimal
  F_pH int [ref: > DataFlags.id] 
  Turb decimal
  F_Turb int [ref: > DataFlags.id] 
  ChlFluor decimal
  F_ChlFluor int [ref: > DataFlags.id]  
}

Table DataFlags {
  id int [pk, increment]
  FlagDescription varchar
}