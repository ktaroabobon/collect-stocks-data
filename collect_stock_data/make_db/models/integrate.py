import pandas as pd
from glob import glob

from make_db.models import download


def read_csv(file_name: str) -> pd.DataFrame:
    """To read csv_file as pd.DataFrame

    Return: pd.DataFrame
    """
    df = pd.read_csv(file_name, encoding='Shift-JIS')
    df.columns = df.iloc[0]
    df.drop(df.index[[0, 1]], inplace=True)

    date_lst = df.values.tolist()
    date_lst = df.reset_index().values.tolist()
    columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'AdjClose']

    new_df = pd.DataFrame(date_lst, columns=columns)
    new_df = new_df.set_index('Date')
    new_df.index = pd.to_datetime(new_df.index, format='%Y-%m-%d')

    new_df[['High', 'Low', 'Open', 'Close', 'Volume', 'AdjClose']]
    return new_df


def get_stock_data_by_year(year: int, files_dict: dict) -> pd.DataFrame:
    """To get stocks_data by a year

    Return: pd.DataFrame
    """
    file_name = files_dict[str(year)]
    df = read_csv(file_name)
    return df


def make_file_dict(files_dict=None) -> dict:
    """To make a dictionary from csv_files

    Return: The dictionary including csv_file_year
    """

    if files_dict is None:
        files_dict = {}

    stock_data_dir = download.get_stock_data_dir_path()
    csv_dir = stock_data_dir + "/*"

    files = glob(csv_dir)
    files.sort()
    for file_name in files:
        files_dict[str(file_name[-8: -4])] = file_name

    return files_dict


def integrate_data(first_year, last_year: int) -> pd.DataFrame:
    """To integrate stocks_data

    Return: pd.DataFrame
    """
    files_dict = make_file_dict()
    df = None

    for year in range(first_year, last_year + 1):
        if df is None:
            try:
                df = get_stock_data_by_year(year, files_dict)
                continue
            except Exception:
                print("Cna't find the {}s file.".format(year))
                continue

        try:
            df = pd.concat(
                [df, get_stock_data_by_year(year, files_dict)], sort=False)
        except Exception:
            print("Cna't find the {}s file.".format(year))

    return df
