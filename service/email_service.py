import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_confirmation_email(to_email, subject, confirmation_code, name, user_id):
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    sender_email = os.getenv('SMTP_EMAIL', '')
    sender_password = os.getenv('SMTP_PASSWORD', '')

    template_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'templates',
        'confirmation_email_template.html'
    )

    print(sender_email, sender_password)

    with open(template_path, "r") as file:
        html_content = file.read()

    confirmation_link = f"http://andrelcarvalho.netlify.app/activate?code={confirmation_code}&id={user_id}"
    html_content = html_content.replace("{{name}}", name)
    html_content = html_content.replace("{{confirmation_code}}", confirmation_code)
    html_content = html_content.replace("{{confirmation_link}}", confirmation_link)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.ehlo()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
            server.close()
        print(f"HTML email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
