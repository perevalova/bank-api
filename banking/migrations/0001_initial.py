# Generated by Django 2.2.10 on 2020-03-11 19:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.UUID('8a787e82-13a7-4d31-8441-678318b58c85'), editable=False, unique=True)),
                ('birthday', models.DateField()),
                ('address', models.CharField(max_length=255)),
                ('passport', models.CharField(max_length=20)),
                ('phone_number', models.CharField(max_length=13)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
