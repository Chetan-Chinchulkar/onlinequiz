# Generated by Django 3.0.5 on 2021-10-09 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0009_course_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='status',
            new_name='taken_status',
        ),
    ]
