import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def load_email_template(template_name, replacements):
    template_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'templates',
        template_name
    )

    try:
        with open(template_path, "r") as file:
            html_content = file.read()

        for placeholder, value in replacements.items():
            html_content = html_content.replace(f"{{{{{placeholder}}}}}", value)

        return html_content
    except FileNotFoundError:
        raise Exception(f"Template file {template_name} not found.")


def send_email(to_email, subject, html_content):
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    sender_email = os.getenv('SMTP_EMAIL', '')
    sender_password = os.getenv('SMTP_PASSWORD', '')

    if not sender_email or not sender_password:
        raise Exception("SMTP credentials are not set in environment variables.")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
            server.close()
        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")


def send_confirmation_email(to_email, subject, confirmation_code, name, user_id):
    base_url = os.getenv('BASE_URL', 'http://localhost')
    confirmation_link = f"{base_url}/activate?code={confirmation_code}&id={user_id}"
    replacements = {
        "name": name,
        "confirmation_code": confirmation_code,
        "confirmation_link": confirmation_link,
    }
    html_content = load_email_template('confirmation_email_template.html', replacements)
    send_email(to_email, subject, html_content)


def send_password_email(to_email, subject, reset_code, name, user_id):
    base_url = os.getenv('BASE_URL', 'http://localhost')
    reset_link = f"{base_url}/reset-password?code={reset_code}&id={user_id}"
    replacements = {
        "name": name,
        "reset_link": reset_link,
    }
    html_content = load_email_template('password_reset_email_template.html', replacements)
    send_email(to_email, subject, html_content)