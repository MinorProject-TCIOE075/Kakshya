# Generated by Django 4.0 on 2022-03-07 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0003_assignment_classroom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentsubmission',
            name='file',
            field=models.FileField(upload_to='media/submission/'),
        ),
    ]
