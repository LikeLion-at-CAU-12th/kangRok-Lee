# Generated by Django 5.0.3 on 2024-04-09 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_alter_comment_writer_alter_post_writer'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(default='0', upload_to='', verbose_name='사진 첨부'),
            preserve_default=False,
        ),
    ]
