# Generated by Django 3.2.5 on 2021-08-01 00:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0004_remove_cafeteria_manager'),
        ('accounts', '0002_alter_worker_worker_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='cafeteria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='workers', to='restaurants.cafeteria'),
        ),
    ]
