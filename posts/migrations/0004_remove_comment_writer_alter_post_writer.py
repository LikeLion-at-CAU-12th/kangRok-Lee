# Generated by Django 5.0.3 on 2024-04-03 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_comment_writer_alter_post_writer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='writer',
        ),
        migrations.AlterField(
            model_name='post',
            name='writer',
            field=models.CharField(max_length=20),
        ),
    ]