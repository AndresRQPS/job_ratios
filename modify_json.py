import json
from job_ratios import job_ratios


def format_json():
    with open('data.json', 'r') as data_file:
        job_data = json.load(data_file)

    formatted_json = []
    data_len = len(job_data)
    job_index = 0

    # Format json data
    while job_index < data_len:
        # Initialize job name and days list
        current_job = job_data[job_index]['Job Name']
        current_obj = {'Job Name': current_job, 'days': []}

        while current_job == job_data[job_index]['Job Name']:
            # Initialize new job object
            days_obj = {'Log Date': job_data[job_index]['Log Date']}

            for count in job_data[job_index]['Counts']:
                days_obj[count['Union Code']] = count['Counts']

            current_obj['days'].append(days_obj)
            job_index += 1
            if job_index >= data_len:
                break

        formatted_json.append(current_obj)

    with open('data.json', 'w') as data_file:
        data_file.write(json.dumps(formatted_json, indent=2))


def add_apprentice_count():
    with open('data.json', 'r') as data_file:
        job_data = json.load(data_file)

    # Check is the APPRENTICE key is in each of the days list
    # If not, add it with a value of zero
    for job in job_data:
        days = job['days']
        for day in days:
            if 'APPRENTICE' not in day.keys():
                day['APPRENTICE'] = 0

    with open('data.json', 'w') as data_file:
        data_file.write(json.dumps(job_data, indent=2))


def add_set_app_journey_counts():
    with open('data.json', 'r') as data_file:
        job_data = json.load(data_file)

    for job in job_data:
        if job['Job Name'] not in job_ratios.keys():
            job['set_apprentice_count'] = 3
            job['set_journey_count'] = 1
            continue

        set_apprentice_count = job_ratios[job['Job Name']]['num_apprentice']
        set_journey_count = job_ratios[job['Job Name']]['num_journeymen']

        job['set_apprentice_count'] = set_apprentice_count
        job['set_journey_count'] = set_journey_count

    with open('data.json', 'w') as data_file:
        data_file.write(json.dumps(job_data, indent=2))


def check_compliant(app_count, journey_count, set_app_count, set_journey_count):
    if app_count == 0 and 1 <= journey_count <= set_journey_count:
        return True

    if journey_count == 1 and app_count == 1:
        return True

    min_journey_count = app_count * set_journey_count

    if min_journey_count <= journey_count <= min_journey_count + set_journey_count:
        return True

    return False


# check if apprentice to journeymen count is compliant on job
def add_compliant():
    with open('data.json', 'r') as data_file:
        job_data = json.load(data_file)

    for job in job_data:
        set_app_count = job['set_apprentice_count']
        set_journey_count = job['set_journey_count']
        for day in job['days']:
            day_apprentice_count = day['APPRENTICE']
            day_journey_count = day['JOURNEY']
            day['is_compliant'] = check_compliant(app_count=day_apprentice_count,
                                                  journey_count=day_journey_count,
                                                  set_app_count=set_app_count,
                                                  set_journey_count=set_journey_count)

    with open('data.json', 'w') as data_file:
        data_file.write(json.dumps(job_data, indent=2))

