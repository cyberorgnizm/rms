# Generated by Django 3.2.5 on 2021-08-08 15:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0007_rename_approved_by_worker_purchaseorder_action_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='student',
        ),
        migrations.RemoveField(
            model_name='purchaseorder',
            name='student',
        ),
        migrations.AddField(
            model_name='invoice',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
    ]
