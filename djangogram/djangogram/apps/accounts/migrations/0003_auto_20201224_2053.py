# Generated by Django 3.1.2 on 2020-12-24 18:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20201218_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpicture',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 24, 18, 53, 3, 225605, tzinfo=utc)),
        ),
    ]