# Generated by Django 3.0.5 on 2021-10-09 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0011_result_result_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='cutoff_marks',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
