# Generated by Django 3.0.5 on 2021-10-09 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0010_auto_20211009_1102'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='result_status',
            field=models.BooleanField(default=False),
        ),
    ]