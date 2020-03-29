from django.core.mail import EmailMessage, get_connection

from bank_project.celery import app
from bank_project.settings import CONTACT_EMAIL
from banking.utils import currency_email


@app.task
def send_currency_email():
    subject, message, emails = currency_email()
    con = get_connection()
    # open connection for mass sending
    con.open()
    for email in emails:
        msg = EmailMessage(subject, message, CONTACT_EMAIL, [email],
                           connection=con)
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()
    con.close()


