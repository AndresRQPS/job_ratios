from sqlStrings import get_server_data
from connectToDatabase import connect_to_qps_database, connect_to_dps_database
from datetime import datetime, timedelta


class ServerData:
    # Get data that only goes back to the last Tuesday
    num_days_back = 7
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
