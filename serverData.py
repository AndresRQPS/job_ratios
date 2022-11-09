from sqlStrings import get_server_data
from connectToDatabase import connect_to_qps_database, connect_to_dps_database
from datetime import datetime, timedelta


def days_till_tuesday():
    today = datetime.now()
    current_day = today.strftime('%A')
    days_until_tuesday = 0

    while current_day != 'Tuesday':
        days_until_tuesday += 1
        current_day = (today - timedelta(days=days_until_tuesday)).strftime('%A')

    return days_until_tuesday


class ServerData:

    # Get data that only goes back to the last Tuesday
    # loop back by one day until it is Tuesday
    # Return then number and pass it to num_days_back
    num_days_back = days_till_tuesday()
    prev_date = datetime.now() - timedelta(days=num_days_back)
    prev_date_str = prev_date.strftime('%d-%b-%y')

    def __init__(self):
        self.data = []

    def get_data(self):
        qps_connection = connect_to_qps_database()
        cursor = qps_connection.cursor()
        cursor.execute(get_server_data(self.prev_date_str))

        server_data = cursor.fetchall()

        self.data = server_data

        if len(self.data) == 0:
            print(f'No data exists for dates through {self.prev_date_str}')
            exit()

