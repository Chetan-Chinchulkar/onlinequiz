# Generated by Django 3.0.5 on 2021-08-02 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0007_course_attempt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='attempt',
        ),
        migrations.RemoveField(
            model_name='result',
            name='attempt',
        ),
    ]
