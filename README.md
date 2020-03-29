# Bank API


## What was implemented

- Make accounts
- Make deposit
- Make withdrawal
- Make transfers
- Make transactions
- View currency exchange rate for USD, EUR, RUR, BTC
- Sending scheduled email with currency exchange rate
- Swagger documentation

### Using

- Python 3.7
- Django 2.2
- Django REST framework 3.11
- Celery 4.4

## Installation

#### 1. Install dependencies:

```bash
pip install -r requirements.txt
```

#### 2. Implement migrations:

```bash
python manage.py migrate
```

#### 3. Run sever:

```bash
python manage.py runserver
```

#### 4. Run redis sever:

```bash
redis-server
```

#### 5. Run celery:

```bash
celery -A bank_project worker -B
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.