# Generated by Django 3.0.5 on 2021-10-09 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0008_auto_20210802_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]