from flask import current_app, render_template
import requests



def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    url = f"https://api.mailgun.net/v3/{app.config['MAILGUN_DOMAIN']}/messages"

    # Mailgun API Key
    auth = ("api", app.config['MAILGUN_KEY'])

    email_data = {
        'subject': app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
        'from': f"{app.config['FLASKY_MAIL_SENDER']} <print@{app.config['MAILGUN_DOMAIN']}>",
        'to': [to],
        'text': render_template(template + '.txt', **kwargs),
        'html': render_template(template + '.html', **kwargs)
    }

    response = requests.post(url, auth=auth, data=email_data)

    # Check if the email was successfully sent
    if response.status_code == 200:
        return True
    else:
        print(f"Error sending email: {response.status_code} - {response.text}")
        return False
