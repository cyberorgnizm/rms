# Generated by Django 3.2.5 on 2021-07-28 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20210724_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseline',
            name='total_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
