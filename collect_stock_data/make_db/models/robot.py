from config import config as cfg
from make_db.models import download, integrate, save
from make_db.views import console


class ConversationRobot(object):

    def __init__(self, speak_color='green',
                 company_name=None, brand_number=None):
        self.speak_color = speak_color
        self.company_name = None
        self.brand_number = None
        self.first_year = None
        self.last_year = None

    def set_company_name(self):
        while True:
            template = console.getTemplate(
                'company_name.txt', self.speak_color
            )
            company_name = input(template.substitute())

            if company_name:
                self.company_name = company_name
                break

    def set_brand_number(self):
        while True:
            template = console.getTemplate(
                'brand_number.txt', self.speak_color
            )
            brand_number = input(template.substitute())

            if brand_number:
                self.brand_number = int(brand_number)
                break

    def set_year(self):
        while True:
            template = console.getTemplate(
                'year.txt', self.speak_color
            )
            year = input(template.substitute())

            if year:
                first_year = int(year[:4])
                last_year = int(year[-4:])
                self.first_year = int(first_year)
                self.last_year = int(last_year)
                break

    def greeting_for_user(self, file_name: str):
        template = console.get_template(
            "{}.txt".format(file_name), self.speak_color
        )

        print(template.substitute())


class StockRobot(ConversationRobot):

    def __init__(self, speak_color='green',
                 company_name=None, brand_number=None):
        super().__init__(speak_color,
                         company_name=company_name,
                         brand_number=brand_number)

    def setting_from_config(self):
        self.company_name, self.brand_number = cfg.get_company_data()
        self.first_year, self.last_year = cfg.get_year_data()

    def to_download_csv(self):
        if (self.first_year is None) or (self.last_year is None):
            self.first_year, self.last_year = cfg.get_year_data()
        if self.brand_number is None:
            _, self.brand_number = cfg.get_company_data()

        download.download_csv(
            first_year=self.first_year,
            last_year=self.last_year,
            brand_number=self.brand_number
        )

    def to_integrate_data(self):
        if (self.first_year is None) or (self.last_year is None):
            self.first_year, self.last_year = cfg.get_year_data()

        df = integrate.integrate_data(
            first_year=self.first_year,
            last_year=self.last_year
        )

        self.df = df

    def to_save(self):
        if self.df is None:
            raise "Can't find the save file."
        if (self.first_year is None) or (self.last_year is None):
            self.first_year, self.last_year = cfg.get_year_data()
        if self.brand_number is None:
            self.company_name, _ = cfg.get_company_data()

        save.save_data(
            company_name=self.company_name,
            brand_number=self.brand_number,
            first_year=self.first_year,
            last_year=self.last_year,
            df=self.df
        )
