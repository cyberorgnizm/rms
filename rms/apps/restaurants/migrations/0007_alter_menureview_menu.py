# Generated by Django 3.2.5 on 2021-08-01 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0006_alter_cafeteriareview_reviewer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menureview',
            name='menu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='restaurants.menu'),
        ),
    ]