from sqlStrings import get_server_data
from connectToDatabase import connect_to_qps_database, connect_to_dps_database


class ServerData:

    def __init__(self):
        self.data = []

    def get_data(self):
        qps_connection = connect_to_qps_database()
        cursor = qps_connection.cursor()
        cursor.execute(get_server_data())

        server_data = cursor.fetchall()

        self.data = server_data
