# Generated by Django 5.0.3 on 2024-04-05 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_comment_post_id_comment_writer_alter_post_writer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='writer',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='post',
            name='writer',
            field=models.CharField(max_length=20),
        ),
    ]
