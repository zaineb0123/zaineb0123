# Generated by Django 2.2.4 on 2021-02-09 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0011_auto_20210209_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likeslist',
            name='idForPost',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='network.Posts'),
        ),
    ]
