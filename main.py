from serverData import ServerData
from local_storage import LocalStorage
import pandas as pd
import json
from send_email import send_email

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


# check if apprentice to journeymen count is compliant on job
def is_compliant(app_amount, journey_amount):
    if app_amount == 0 and 1 <= journey_amount <= 3:
        return True

    min_journey_count = app_amount * 3

    if min_journey_count <= journey_amount <= min_journey_count + 3:
        return True

    return False


# Add if job is compliant (Yes, No)
with open('data.json') as file:
    data_dict = json.load(file)

for record in data_dict:

    apprentice_count = 0
    journey_count = 0
    for count in record['Counts']:

        if count['Union Code'] == 'APPRENTICE':
            apprentice_count = count['Counts']

        if count['Union Code'] == 'JOURNEY':
            journey_count = count['Counts']

    if apprentice_count == 0:
        record['Counts'].append({"Union Code": "APPRENTICE", "Counts": 0})

    # Check if apprentice to journeymen count is compliant
    record['is_compliant'] = is_compliant(apprentice_count, journey_count)

with open('data.json', 'w') as outfile:
    outfile.write(json.dumps(data_dict, indent=2))

# Load in json data
with open('data.json', 'r') as data_file:
    data = json.load(data_file)


formatted_json = []
data_len = len(data)
job_index = 0

# Format json data
while job_index < data_len:
    # Initialize job name and days list
    current_job = data[job_index]['Job Name']
    current_obj = {'Job Name': current_job, 'days': []}

    while current_job == data[job_index]['Job Name']:
        # Initialize new job object
        days_obj = {'Log Date': data[job_index]['Log Date']}

        for count in data[job_index]['Counts']:
            days_obj[count['Union Code']] = count['Counts']

        days_obj['is_compliant'] = data[job_index]['is_compliant']

        current_obj['days'].append(days_obj)
        job_index += 1
        if job_index >= data_len:
            break

    formatted_json.append(current_obj)

with open('data.json', 'w') as outfile:
    outfile.write(json.dumps(formatted_json, indent=2))

send_email()
