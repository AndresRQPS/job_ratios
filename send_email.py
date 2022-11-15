import dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json


def highlight(is_compliant_bool):
    return 'style="color:red;"' if not is_compliant_bool else ''


def compile_html():
    # Get json data
    html_string = '''
    <html>
        <head></head>
        <body>
          <p>Good morning Rachel and Nela,</p>
    '''
    # Loop though jobs
    with open('data.json', 'r') as data_csv:
        data = json.load(data_csv)

    for index, job in enumerate(data):
        # Job title
        html_string += f'<h2>{job["Job Name"]}</h2>\n'
        html_string += f'<p>Set Ratio: {job["set_apprentice_count"]} Apprentice to {job["set_journey_count"]} Journeymen</p>\n'

        for day in job['days']:
            if 'JOURNEY' not in day.keys():
                print(f'There is no journeymen in {day["Job Name"]}')
                exit()

            html_string += f'<h4>{day["Log Date"]}</h4>'
            html_string += f'''
            <ul>
                <li>Apprentice - {day["APPRENTICE"]}</li>
                <li>Journey - {day["JOURNEY"]}</li>
                <li {highlight(day['is_compliant'])} >Compliant - {'Yes' if day['is_compliant'] else 'No'}
            </ul>
            '''

        if index < len(data) - 1:
            html_string += '<p>========================================================</p>'

    html_string += '''
            <p>Best,</p>
            <p>Andres Rodriguez <br>
            Systems Analyst</p>
        </body>
    </html>
    '''
    return html_string


def send_email():
    config = dotenv.dotenv_values(".env")

    office_emails = ['rachelg@qpscompany.com', 'nelan@qpscompany.com', 'andresr@qpscompany.com']

    my_email = config["EMAILUSERNAME"]
    my_password = config["EMAILPASSWORD"]

    sender = "andresr@qpscompany.com"
    receivers = office_emails
    # receivers = ['andresr@qpscompany.com']

    message = MIMEMultipart("alternative")
    message["Subject"] = "Certified Job Ratios"
    message["From"] = sender
    message["To"] = ', '.join(receivers)

    html = compile_html()

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(html, "html")

    # Attach parts into message container.
    message.attach(part1)

    try:
        smtp_obj = smtplib.SMTP("mail2.qpscompany.com", 587)
        smtp_obj.starttls()
        smtp_obj.login(my_email, my_password)
        smtp_obj.sendmail(sender, receivers, message.as_string())
        smtp_obj.close()

        print("Successfully sent email")
    except Exception as e:
        print(e)
