import requests

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.template.loader import render_to_string

from datetime import date


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def get_currency():
    """ Cache currency exchange rate """
    if 'currency' in cache:
        currency = cache.get('currency') # get results from cache
    else:
        url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=11'
        currency = requests.get(url)
        cache.set('currency', currency, timeout=CACHE_TTL) # store data in cache
    return currency


def currency_email():
    """
    Send letter to user about currency exchange rate
    :return: subject, message, list of users' email
    """
    users_email = list(get_user_model().objects.values_list('email', flat=True))
    current_date = date.today().strftime("%d %B %Y")
    subject = f'Currency rate on {current_date}'

    currency_list = get_currency().json()
    message = render_to_string('currency_rate.html', {
        'object_list': currency_list
    })
    return subject, message, users_email