import dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json


def compile_html():
    # Get json data
    html_string = '''
    <html>
        <head></head>
        <body>
          <p>Good morning Rachel and Nela,</p>
          <p>Ratio = Apprentice / Journeymen</p>
    '''
    # Loop though jobs
    with open('data.json', 'r') as data_csv:
        data = json.load(data_csv)

    def highlight(set_ratio, day_ratio):
        return 'style="color:red;"' if day_ratio > set_ratio else ''

    for index, job in enumerate(data):
        # Job title
        html_string += f'<h2>{job["Job Name"]}</h2>\n'
        html_string += f'<p>Set Ratio: {job["set_app"]} Apprentice to {job["set_journey"]} Journeymen ({job["set_ratio"]})</p>\n'

        for day in job['days']:
            html_string += f'<h4>{day["Log Date"]}</h4>'
            html_string += f'''
            <ul>
                <li>Apprentice - {day["APPRENTICE"]}</li>
                <li>Journey - {day["JOURNEY"]}</li>
                <li {highlight(set_ratio=job['set_ratio'], day_ratio=day['day_ratio'])}>Ratio - {day["day_ratio"]}</li>
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
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
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
