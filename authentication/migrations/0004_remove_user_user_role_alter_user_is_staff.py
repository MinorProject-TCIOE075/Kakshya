# Generated by Django 4.0 on 2022-02-07 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_user_user_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user_role',
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status'),
        ),
    ]