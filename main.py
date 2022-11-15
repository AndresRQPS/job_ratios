from serverData import ServerData
from local_storage import LocalStorage
import pandas as pd
from send_email import send_email
from modify_json import format_json, add_apprentice_count, add_set_app_journey_counts, add_compliant

local_storage = LocalStorage()
file_data = ''
# Check is server file is created
if not local_storage.server_data_exists():
    server_data = ServerData()
    server_data.get_data()
    print('Pulled data from server')
    local_storage.save_server_data(server_data.data)
    local_storage.stamp_current_date()
    file_data = local_storage.get_file_data()
else:
    # Check if data was pulled today
    if local_storage.pulled_data_today():
        file_data = local_storage.get_file_data()
        print('Pulled data from csv file')
    else:
        server_data = ServerData()
        server_data.get_data()
        print('Pulled data from server')
        local_storage.save_server_data(server_data.data)
        local_storage.stamp_current_date()
        file_data = local_storage.get_file_data()

# Find number of jouneyman to apprentice in jobs
union_code_filt = file_data['Union Code'].isin(['C4A'])
job_date_group_df: pd.DataFrame = file_data.loc[~union_code_filt]

# Remove duplicates by employee_code, job_id, and Log Date
job_date_group_df = job_date_group_df.drop_duplicates(subset=['employee_code', 'job_id', 'Log Date'])

app_filt = (job_date_group_df['Union Code'].isin(['1ST-NEW', '2ND-NEW',
                                                  '3RD', '4TH-NEW',
                                                  '5TH-NEW', '6TH-NEW',
                                                  '7TH-NEW', '8TH', '8TH-NEW']))
job_date_group_df.loc[app_filt, 'Union Code'] = 'APPRENTICE'

journey_filt = job_date_group_df['Union Code'].isin(['FOREMEN'])
job_date_group_df.loc[journey_filt, 'Union Code'] = 'JOURNEY'

job_date_group_gp = job_date_group_df.groupby(['Job Name', 'Log Date'])

# Get num of journeymen for each group
journey_to_apps = job_date_group_gp['Union Code']\
    .value_counts()\
    .rename_axis(['Job Name', 'Log Date', 'Union Code'])\
    .reset_index(name='Counts')

journey_to_apps.groupby(['Job Name', 'Log Date'], group_keys=True)\
    .apply(lambda x: x[['Union Code', 'Counts']].to_dict('records'))\
    .reset_index().rename(columns={0: 'Counts'})\
    .to_json('data.json', orient='records')

format_json()

add_apprentice_count()

add_set_app_journey_counts()

add_compliant()

send_email()
