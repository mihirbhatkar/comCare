# Generated by Django 3.2.10 on 2022-04-18 18:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_auto_20220418_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='resolve_msg',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='notice',
            name='showtill',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 20, 0, 6, 43, 656886)),
        ),
    ]
