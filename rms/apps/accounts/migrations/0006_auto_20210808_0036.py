# Generated by Django 3.2.5 on 2021-08-08 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20210808_0019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_lecturer',
            field=models.BooleanField(default=False, help_text='Designates whether the user is alecturer'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_student',
            field=models.BooleanField(default=False, help_text='Designates whether the user is a student'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_worker',
            field=models.BooleanField(default=False, help_text='Designates whether the user is a worker in any of the college cafeteria'),
        ),
    ]
