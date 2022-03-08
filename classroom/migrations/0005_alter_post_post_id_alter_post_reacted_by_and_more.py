# Generated by Django 4.0 on 2022-03-06 15:04

from django.conf import settings
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('classroom', '0004_classroom_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_id',
            field=models.UUIDField(default=uuid.UUID('45337bbf-3820-443f-b06d-491c6e8ca65b'), unique=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='reacted_by',
            field=models.ManyToManyField(blank=True, related_name='post_reactors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='reacts',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
