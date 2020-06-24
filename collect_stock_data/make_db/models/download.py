from selenium import webdriver
import time
import os

from config import config as cfg


def get_stock_data_dir_path() -> str:
    """To Research and Return the path of the stock_data directory.

    Returns: The dir path.
    """
    dir_path = None

    if not dir_path:
        base_dir = os.path.dirname(os.getcwd())

        dir_path = os.path.join(base_dir, 'stock_data')
        os.makedirs(dir_path, exist_ok=True)

    return dir_path


def enable_download_in_headless_chrome(driver) -> None:
    """To be able to download csv_files at Google Chrome in headless mode"""
    driver.command_executor._commands["send_command"] = (
        "POST", '/session/$sessionId/chromium/send_command')

    stock_data_dir = get_stock_data_dir_path()

    params = {'cmd': 'Page.setDownloadBehavior', 'params': {
        'behavior': 'allow', 'downloadPath': stock_data_dir}}
    driver.execute("send_command", params)


def setting_chrome():
    """To set up browser option.

    * Here, browser is Google Chrome.
    """
    stock_data_dir = get_stock_data_dir_path()
    options = webdriver.chrome.options.Options()
    options.add_argument('--headless')
    options.add_experimental_option("prefs", {
        "download.default_directory": stock_data_dir
    })

    chromedriver_path = cfg.get_chromedriver()
    browser = webdriver.Chrome(chromedriver_path, chrome_options=options)
    enable_download_in_headless_chrome(browser)
    browser.implicitly_wait(3)

    return browser


def access_internet(year, brand_number: int) -> None:
    """To access the data_site you choose by brand_number and year."""
    if brand_number is None:
        _, brand_number = cfg.get_company_data(string=True)

    url = "https://kabuoji3.com/stock/{}/{}/".format(
        str(brand_number), str(year))

    browser = setting_chrome()
    try:
        browser.get(str(url))
    except Exception:
        raise "Can't access such Web Page."

    browser.find_element_by_name("csv").click()

    browser.find_element_by_name("csv").click()

    time.sleep(5)

    browser.quit()


def download_csv(first_year, last_year, brand_number: int) -> None:
    """To download csv_file from the Internet."""
    for year in range(first_year, last_year+1):
        try:
            access_internet(year, brand_number)
        except Exception:
            pass
