# Generated by Django 3.2.5 on 2021-07-11 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cafeteria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cafeteria_name', models.CharField(max_length=255)),
                ('cafeteria_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('cafeteria_image', models.ImageField(upload_to='cafeterias')),
                ('cafeteria_address', models.TextField()),
                ('cafeteria_work_hours', models.DurationField()),
                ('cafeteria_manager', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.worker')),
            ],
        ),
        migrations.CreateModel(
            name='CafeteriaMenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_name', models.CharField(max_length=255)),
                ('menu_image', models.ImageField(upload_to='products')),
                ('menu_description', models.TextField()),
                ('menu_slug', models.SlugField(blank=True, unique=True)),
                ('menu_type', models.CharField(choices=[('food', 'Food'), ('drink', 'Drink'), ('snack', 'Snack')], max_length=255)),
                ('menu_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('menu_discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('cafeteria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.cafeteria')),
            ],
            options={
                'verbose_name_plural': 'Menus',
            },
        ),
        migrations.CreateModel(
            name='MenuReview',
            fields=[
                ('review_id', models.UUIDField(primary_key=True, serialize=False)),
                ('review_ratings', models.DecimalField(decimal_places=1, max_digits=5)),
                ('review_comments', models.TextField(blank=True, null=True)),
                ('review_menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.cafeteriamenu')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
            ],
        ),
        migrations.CreateModel(
            name='CafeteriaReview',
            fields=[
                ('review_id', models.UUIDField(primary_key=True, serialize=False)),
                ('review_ratings', models.DecimalField(decimal_places=1, max_digits=5)),
                ('review_comments', models.TextField(blank=True, null=True)),
                ('review_menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.cafeteria')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
            ],
        ),
    ]
