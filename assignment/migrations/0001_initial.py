# Generated by Django 4.0 on 2022-02-26 14:55

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0002_initial'),
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('due_date', models.DateTimeField()),
                ('title', models.CharField(max_length=100)),
                ('details', models.CharField(max_length=250)),
                ('file', models.FileField(upload_to='assignments/')),
                ('close_date', models.DateTimeField()),
                ('points', models.IntegerField()),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('modified_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.course')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.user')),
            ],
        ),
        migrations.CreateModel(
            name='AssignmentSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='submitted', max_length=50)),
                ('grade', models.IntegerField(default=0)),
                ('file', models.FileField(upload_to='submission/')),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('modified_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('assignment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assignment.assignment')),
                ('submitted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.user')),
            ],
        ),
    ]
