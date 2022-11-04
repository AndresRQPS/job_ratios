def get_server_data():
    sql_server_data = '''
    SELECT
        labor.employee_code,
        e.name,
        labor.job_id,
        j.job_number,
        j.loc_name,
        labor.union_code,
        labor.log_date,
        labor.device_code,
        labor.quantity
    FROM
        labor_time_log_stage_data labor
    LEFT JOIN
        employees e
    ON
        labor.employee_code = e.code
    LEFT JOIN
        jobs j
    ON
        labor.job_id = j.job_id
    WHERE
        labor.log_date >= '01-NOV-22'
    AND
        labor.union_code NOT IN ('FOREMEN', 'STOC-NEW', 'C4A')
    '''
    return sql_server_data
