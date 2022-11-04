import pandas
import os
from datetime import datetime


class LocalStorage:
    SERVER_DATA_FILE = 'server_data.csv'
    DATE_FILE = 'date_file.txt'

    def __init__(self):
        pass

    def get_file_data(self):
        return pandas.read_csv(self.SERVER_DATA_FILE)

    def pulled_data_today(self):
        date_in_file = self.get_file_date()
        if date_in_file == datetime.now().strftime('%d-%b-%y'):
            return True
        else:
            return False

    def get_file_date(self):
        with open(self.DATE_FILE, 'r') as date_file:
            return date_file.read()

    def save_server_data(self, server_data):
        server_data_dataframe = pandas.DataFrame(server_data)
        server_data_dataframe.to_csv(self.SERVER_DATA_FILE, header=['employee_code',
                                                                    'name',
                                                                    'job_id',
                                                                    'job_number',
                                                                    'Job Name',
                                                                    'Union Code',
                                                                    'Log Date',
                                                                    'device_code',
                                                                    'quantity'])

    def server_data_exists(self):
        return os.path.exists(self.SERVER_DATA_FILE)

    def stamp_current_date(self):
        with open(self.DATE_FILE, 'w') as date_file:
            date_file.write(f"{datetime.now().strftime('%d-%b-%y')}")
