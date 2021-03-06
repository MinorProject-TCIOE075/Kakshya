# Generated by Django 4.0.2 on 2022-02-11 14:00

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.manager
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='email address')),
                ('user_type', models.CharField(choices=[('Student', 'Student'), ('Teacher', 'Teacher')], max_length=20)),
                ('phone_num', models.CharField(blank=True, max_length=14, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Date of Birth')),
                ('blood_group', models.CharField(blank=True, max_length=4, null=True, verbose_name='Blood Group')),
                ('citizenship_num', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Citizenship Number')),
                ('add_email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Additional Email')),
                ('add_phone_num', models.CharField(blank=True, max_length=14, null=True)),
            ],
            options={
                'permissions': [('post_notice', 'can post notices about classes'), ('assign_assignments', 'can assign assignments to students')],
            },
            managers=[
                ('users', django.db.models.manager.Manager()),
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_permanent', models.BooleanField(default=True)),
                ('address', models.CharField(blank=True, max_length=150, null=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year_joined', models.DateField(blank=True, null=True)),
                ('roll_number', models.CharField(blank=True, max_length=12, null=True, unique=True)),
                ('classrooms', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(blank=True, max_length=100, null=True)),
                ('year_joined', models.DateField(blank=True, null=True)),
                ('classrooms', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
