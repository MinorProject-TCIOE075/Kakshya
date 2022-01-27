# Generated by Django 4.0 on 2022-01-21 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='DailyRoutine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('day', models.CharField(choices=[('SUN', 'Sunday'), ('MON', 'Monday'), ('TUE', 'Tuesday'), ('WED', 'Wednesday'), ('THU', 'Thursday'), ('FRI', 'Friday'), ('SAT', 'Saturday')], max_length=10)),
                ('program', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='routine.program')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('is_cancelled', models.BooleanField(default=False)),
                ('cancelled_by', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cancelled_courses', to='authentication.user')),
                ('daily_routine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='routine.dailyroutine')),
                ('subject_teacher', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='authentication.user')),
            ],
        ),
    ]