from config import config as cfg
from make_db.models import download

import os
import pandas as pd
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative
import shutil


def get_save_dir_path() -> str:
    """To Research and Return the path of the directory you choose.

    Returns: The dir path.
    """
    db_house_path = None

    if not db_house_path:
        base_dir = os.path.dirname(os.getcwd())

        dir_path = os.path.join(base_dir, "company_stock_data")
        os.makedirs(dir_path, exist_ok=True)

    return dir_path


def save_sql(file_format, company_name: str,
             df: pd.DataFrame) -> None:
    """To save stock_data file in MYSQL."""
    if file_format == "MYSQL":
        database_name = cfg.get_database_name(file_format)
        engine = sqlalchemy.create_engine(
            'mysql+pymysql://root:@localhost/{}'.format(database_name))
    elif file_format == 'sqlite3':
        database_name = cfg.get_database_name(file_format)
        save_dir_path = get_save_dir_path()
        database_path = os.path.join(save_dir_path, database_name)
        engine = sqlalchemy.create_engine(
            'sqlite:///{}.db'.format(database_path))

    Base = sqlalchemy.ext.declarative.declarative_base()

    class StockData(Base):
        __tablename__ = company_name
        Date = sqlalchemy.Column(
            sqlalchemy.DateTime, primary_key=True)
        High = sqlalchemy.Column(sqlalchemy.Integer)
        Low = sqlalchemy.Column(sqlalchemy.Integer)
        Open = sqlalchemy.Column(sqlalchemy.Integer)
        Close = sqlalchemy.Column(sqlalchemy.Integer)
        Volume = sqlalchemy.Column(sqlalchemy.Integer)
        AdjClose = sqlalchemy.Column(sqlalchemy.Integer)

    Base.metadata.create_all(engine)

    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()

    for index, row in df.iterrows():
        date = index.to_pydatetime()
        high = row['High']
        low = row['Low']
        opn = row['Open']
        close = row['Close']
        volume = row['Volume']
        adjclose = row['AdjClose']

        data = StockData(Date=date, High=high, Low=low, Open=opn,
                         Close=close, Volume=volume, AdjClose=adjclose)
        session.add(data)
    session.commit()


def save_csv(company_name, file_name: str, df: pd.DataFrame) -> None:
    """To save stock_data file as CSV_file."""
    save_base_dir_path = get_save_dir_path()
    file_path = os.path.join(save_base_dir_path, company_name, file_name)

    df.to_csv(file_path)


def save_data(company_name: str,
              first_year, last_year: int,
              df: pd.DataFrame) -> None:
    """Swich about save file format."""
    file_format = cfg.get_file_format()

    if file_format == "MYSQL" or file_format == "sqlite3":
        save_sql(file_format, company_name, df)
    else:
        file_name = "{}_{}-{}.csv".format(company_name, first_year, last_year)
        save_csv(company_name, file_name, df)

    dir_path = download.get_stock_data_dir_path()
    shutil.rmtree(dir_path)
