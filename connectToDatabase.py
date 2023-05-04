import oracledb
from dotenv import dotenv_values

config = dotenv_values('.env')

USERNAME = config['DBUSERNAME']
PASSWORD = config['DBPASSWORD']
IPADDRESS = config['IPADDRESS']
PORT = config['PORT']
QPSSERVERNAME = config['QPSSERVERNAME']
DPSSERVERNAME = config['DPSSERVERNAME']


def connect_to_qps_database():
    oracledb.init_oracle_client()
    try:
        connection = oracledb.connect(f'{USERNAME}/{PASSWORD}@//{IPADDRESS}:{PORT}/{QPSSERVERNAME}')
        return connection
    except Exception as e:
        print('Connection to QPS database failed')
        print(e)


def connect_to_dps_database():
    oracledb.init_oracle_client()
    try:
        connection = oracledb.connect(f'{USERNAME}/{PASSWORD}@//{IPADDRESS}:{PORT}/{DPSSERVERNAME}')
        return connection
    except Exception as e:
        print("Connection to DPS database failed")
        print(e)
