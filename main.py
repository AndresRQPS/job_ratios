from serverData import ServerData
from local_storage import LocalStorage
import pandas as pd

local_storage = LocalStorage()
file_data = ''
# Check is server file is created
if not local_storage.server_data_exists():
    server_data = ServerData()
    server_data.get_data()
    local_storage.save_server_data(server_data.data)
    local_storage.stamp_current_date()
    file_data = local_storage.get_file_data()
else:
    # Check if data was pulled today
    if local_storage.pulled_data_today():
        file_data = local_storage.get_file_data()
    else:
        server_data = ServerData()
        server_data.get_data()
        local_storage.save_server_data(server_data.data)
        local_storage.stamp_current_date()
        file_data = local_storage.get_file_data()

# Find number of jouneyman to apprentice in jobs
union_code_filt = file_data['Union Code'].isin(['C4A', 'FOREMEN'])
job_date_group_df: pd.DataFrame = file_data.loc[~union_code_filt]

app_filt = (job_date_group_df['Union Code'].isin(['1ST-NEW', '2ND-NEW',
                                                  '3RD', '4TH-NEW',
                                                  '5TH-NEW', '6TH-NEW',
                                                  '7TH-NEW', '8TH', '8TH-NEW']))
job_date_group_df.loc[app_filt, 'Union Code'] = 'APPRENTICE'

job_date_group_gp = job_date_group_df.groupby(['Job Name', 'Log Date'])\
    .apply(lambda x: x[['Union Code']].to_dict('records'))\
    .reset_index().to_json('data.json', orient='records')


# # Get num of journeymen for each group
# journey_to_apps = job_date_group_gp['Union Code'].value_counts()
# journey_to_apps.to_excel('data.xlsx')
