from make_db.controllers import controller

if __name__ == '__main__':

    import os
    os.chdir(
        "/Users/ktaroabobon/programming/Python3/実践/株価/GoogleSheets/collect_stock_data")

    controller.controller_make_database()
