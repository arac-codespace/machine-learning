from database_operations.models import Base
from sqlalchemy import create_engine


def create_db_engine():
    server = r"DESKTOP-4IL536V\SQLEXPRESS"
    database = r"nerr_database"
    conn_str = f"mssql+pyodbc://{server}/{database}?driver=SQL+Server+Native+Client+11.0"
    engine = create_engine(conn_str)
    return engine


def create_database_schema():
    engine = create_db_engine()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_database_schema()
