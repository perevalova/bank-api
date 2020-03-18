from rest_framework import status
from rest_framework.exceptions import APIException


class InvalidAccountReceiver(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Account of receiver is inactive or blocked.'
    default_code = 'account_error'


class InvalidAccount(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'You can\'t send money to your own account.'
    default_code = 'account_error'


class InvalidAmount(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Not enough money on balance.'
    default_code = 'amount_error'
