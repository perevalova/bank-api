# Generated by Django 2.2.10 on 2020-03-28 10:31

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('banking', '0004_auto_20200317_2129'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('10.00'))])),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(blank=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banking.Account')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
