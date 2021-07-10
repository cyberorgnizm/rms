# Generated by Django 3.2.5 on 2021-07-10 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210710_1334'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='admission_year',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='student_department',
            field=models.CharField(choices=[('computer science', 'Computer Science'), ('mass communication', 'Mass communication'), ('anatomy', 'Anatomy')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1, verbose_name='gender'),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_level',
            field=models.CharField(choices=[('100', '100 Level'), ('200', '200 Level'), ('300', '300 Level'), ('400', '400 Level')], max_length=255, verbose_name='level'),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_matric',
            field=models.CharField(max_length=255, verbose_name='matriculation number'),
        ),
    ]
