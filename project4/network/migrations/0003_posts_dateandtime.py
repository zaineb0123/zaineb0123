# Generated by Django 2.2.4 on 2021-01-11 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_posts'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='dateAndTime',
            field=models.DateTimeField(null=True),
        ),
    ]
