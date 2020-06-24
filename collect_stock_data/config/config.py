import configparser


def conversation_setting() -> str:
    config = configparser.ConfigParser()
    config.read('config.ini')

    conversation = config['setting']['conversation']
    return conversation


def get_company_data(string=False) -> (str, int):
    """To get company_data by the config_file.

    Return: (
        company_name = str,
        brand_number = int
        )
    """
    config = configparser.ConfigParser()
    config.read('config.ini')

    company_name = config['company_data']['company_name']
    brand_name = config['company_data']['brand_number']

    if string:
        return company_name, brand_name
    else:
        return company_name, int(brand_name)


def get_year_data(string=False) -> (int, int):
    """To get year_data by the config_file.

    Return: (
        first_year: int,
        last_year: int
        )
    """

    config = configparser.ConfigParser()
    config.read('config.ini')

    first_year = config['year_data']['first_year']
    last_year = config['year_data']['last_year']

    if string:
        return first_year, last_year
    else:
        return int(first_year), int(last_year)


def get_chromedriver() -> str:
    """To get the chromedriver path"""
    config = configparser.ConfigParser()
    config.read('config.ini')

    chromedriver_path = config['chromedriver']['path']

    return chromedriver_path


def get_file_format() -> int:
    """Which file format to save"""
    config = configparser.ConfigParser()
    config.read('config.ini')

    file_format = "csv"
    print(config['save_format'].getboolean('mysql'))
    print(config['save_format'].getboolean('sqlite3'))

    if config['save_format'].getboolean('mysql'):
        file_format = "MYSQL"
    elif config['save_format'].getboolean('sqlite3'):
        file_format = "sqlite3"

    return file_format


def get_database_name(file_format: str) -> str:
    config = configparser.ConfigParser()
    config.read('config.ini')

    if file_format == "MYSQL":
        database_name = config['mysql_info']['database_name']
    elif file_format == "sqlite3":
        database_name = config['sqlite3_info']['database_name']

    return database_name
