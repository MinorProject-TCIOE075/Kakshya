# Generated by Django 4.0 on 2022-03-07 14:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0007_comment_commented_by_alter_comment_comment_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_id',
            field=models.UUIDField(default=uuid.UUID('31423806-23f9-4df1-bbee-0c93397126b0'), unique=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_id',
            field=models.UUIDField(default=uuid.UUID('a6d3fa39-0866-411d-9717-a39e22820037'), unique=True),
        ),
    ]
