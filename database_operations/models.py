from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Numeric, DateTime

Base = declarative_base()


class Stations(Base):
    __tablename__ = "sampling_stations"

    id = Column(Integer, autoincrement=True)
    StationCode = Column(String(64), primary_key=True, nullable=False)
    NERRSiteID = Column(String(64))
    StationName = Column(String(64))
    Latitude = Column(Numeric)
    Longitude = Column(Numeric)
    Status = Column(String(128))
    ActiveDates = Column(String)
    State = Column(String(64))
    ReserveName = Column(String(128))
    GMTOffset = Column(String(64))
    ParametersReported = Column(String(256))

    def __repr__(self):
        return "<Stations(StationCode='%s')>" % (self.StationCode)


class Timeseries(Base):
    __abstract__ = True
    id = Column(Integer, autoincrement=True)
    StationCode = Column(String(64), primary_key=True, nullable=False)
    DateTimeStamp = Column(DateTime)
    Historical = Column(Integer)
    ProvisionalPlus = Column(Integer)


class WaterQuality(Timeseries):
    __tablename__ = 'water_quality'

    F_Record = Column(Integer)
    Temp = Column(Float)
    F_Temp = Column(Integer)
    SpCond = Column(Float)
    F_SpCond = Column(Integer)
    Sal = Column(Float)
    F_Sal = Column(Integer)
    DO_Pct = Column(Float)
    F_DO_Pct = Column(Integer)
    DO_mgl = Column(Float)
    F_DO_mgl = Column(Integer)
    Depth = Column(Float)
    F_Depth = Column(Integer)
    cDepth = Column(Float)
    F_cDepth = Column(Integer)
    Level = Column(Float)
    F_Level = Column(Integer)
    cLevel = Column(Float)
    F_cLevel = Column(Integer)
    pH = Column(Float)
    F_pH = Column(Integer)
    Turb = Column(Float)
    F_Turb = Column(Integer)
    ChlFluor = Column(Float)
    F_ChlFluor = Column(Integer)

    def __repr__(self):
        return "<WaterQuality(StationCode='%s')>" % (self.StationCode)


class Nutrients(Timeseries):
    __tablename__ = 'nutrients'

    REP = Column(String(64))
    F_Record = Column(Integer)
    PO4F = Column(Float)
    F_PO4F = Column(Integer)
    NH4F = Column(Float)
    F_NH4F = Column(Integer)
    NO2F = Column(Float)
    F_NO2F = Column(Integer)
    NO3F = Column(Float)
    F_NO3F = Column(Integer)
    NO23F = Column(Float)
    F_NO23F = Column(Integer)
    CHLA_N = Column(Float)
    F_CHLA_N = Column(Integer)

    def __repr__(self):
        return "<Nutrients(StationCode='%s')>" % (self.StationCode)


class Weather(Timeseries):
    __tablename__ = 'weather'

    Frequency = Column(Integer)
    F_Record = Column(Integer)
    ATemp = Column(Float)
    F_ATemp = Column(Integer)
    RH = Column(Float)
    F_RH = Column(Integer)
    BP = Column(Float)
    F_BP = Column(Integer)
    WSpd = Column(Float)
    F_WSpd = Column(Integer)
    MaxWSpd = Column(Float)
    F_MaxWSpd = Column(Integer)
    MaxWSpdT = Column(String(64))
    Wdir = Column(Float)
    F_Wdir = Column(Integer)
    SDWDir = Column(Float)
    F_SDWDir = Column(Integer)
    TotPAR = Column(Float)
    F_TotPAR = Column(Integer)
    TotPrcp = Column(Float)
    F_TotPrcp = Column(Integer)
    TotSoRad = Column(Float)
    F_TotSoRad = Column(Integer)

    def __repr__(self):
        return "<Weather(StationCode='%s')>" % (self.StationCode)
