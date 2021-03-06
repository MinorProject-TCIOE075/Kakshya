# Generated by Django 4.0 on 2022-03-07 14:36

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0008_alter_comment_comment_id_alter_post_post_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_id',
            field=models.UUIDField(default=uuid.UUID('8dcb060d-8c15-431e-836b-7b072c551f25'), unique=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_id',
            field=models.UUIDField(default=uuid.UUID('bc635232-8ee7-448c-ab5b-0ccdfea078be'), unique=True),
        ),
    ]
