# Generated by Django 4.0 on 2022-01-19 15:06

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0010_alter_department_modified_on_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='modified_on',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 1, 19, 15, 6, 22, 878732, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='modified_on',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 1, 19, 15, 6, 22, 879931, tzinfo=utc), null=True),
        ),
    ]
