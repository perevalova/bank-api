import requests
from django.contrib.auth import get_user_model
from datetime import date

from django.template.loader import render_to_string


def currency_email():
    """
    Send letter to user about currency exchange rate
    :return: subject, message, list of users' email
    """
    users_email = list(get_user_model().objects.values_list('email', flat=True))
    current_date = date.today().strftime("%d %B %Y")
    subject = f'Currency rate on {current_date}'
    url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=11'
    currency = requests.get(url)
    currency_list = currency.json()
    message = render_to_string('currency_rate.html', {
        'object_list': currency_list
    })
    return subject, message, users_email