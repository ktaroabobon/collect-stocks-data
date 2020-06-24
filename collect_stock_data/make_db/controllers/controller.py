from make_db.models import robot
from config import config as cfg


def controller_make_database(brand_number=None, company_name=None):
    stock_robot = robot.StockRobot()
    stock_robot.greeting_for_user("hello")

    if cfg.conversation_setting() == "True":
        stock_robot.set_company_name()
        stock_robot.set_brand_number()
        stock_robot.set_year()
    else:
        stock_robot.setting_from_config()

    stock_robot.greeting_for_user("collecting_now")

    stock_robot.to_download_csv()
    stock_robot.to_integrate_data()
    stock_robot.to_save()

    stock_robot.greeting_for_user("good_bye")
