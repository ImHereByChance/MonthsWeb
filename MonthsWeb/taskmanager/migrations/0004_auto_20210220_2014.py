# Generated by Django 3.1.6 on 2021-02-20 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0003_auto_20210220_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='autoshift',
            field=models.BooleanField(default=False),
        ),
    ]
