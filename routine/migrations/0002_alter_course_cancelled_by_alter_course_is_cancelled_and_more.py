# Generated by Django 4.0 on 2022-01-21 21:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('routine', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='cancelled_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cancelled_courses', to='authentication.user'),
        ),
        migrations.AlterField(
            model_name='course',
            name='is_cancelled',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='subject_teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='authentication.user'),
        ),
    ]
