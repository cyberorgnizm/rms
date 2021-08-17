import os
import datetime
import pandas as pd
from django.db.models.signals import post_migrate
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.dispatch import receiver
from django.apps import apps
from .models import Cafeteria, Menu


restaurants_app = apps.get_app_config('restaurants')


@receiver(post_migrate, sender=restaurants_app)
def create_restaurants(sender, **kwargs):
    print("Deleting cafeterias...")
    Cafeteria.objects.all().delete()
    print("Successfully removed all cafeterias")
    cafeteria_df = pd.read_csv(f'{restaurants_app.path}/data/restaurants.csv', index_col=0)
    
    for _, record in cafeteria_df.iterrows():
        print(f"Creating cafeteria record for {record['name']}")
        cafeteria = Cafeteria(
            name=record["name"],
            email=record["email"],
            address=record["address"],
            opening_hour=datetime.time(8,0,0),
            closing_hour=datetime.time(22,0,0)
        )
        # read image file as binary using filepath to update cafeteria image
        with open(f"{settings.BASE_DIR}/rms/{record['image']}", "rb") as file:
            upload_file = SimpleUploadedFile(name=str(file.name), content=file.read())
            cafeteria.image = upload_file
        cafeteria.save()
        print(f"Successfully created cafeteria {record['name']}")




@receiver(post_migrate, sender=restaurants_app)
def create_menus(sender, **kwargs):
    # clear table
    Menu.objects.all().delete()
    menu_df = pd.read_csv(f'{restaurants_app.path}/data/menus.csv', index_col=0)
    
    for _, record in menu_df.iterrows():
        print(f"Creating {record['name']} menu record for {record['cafeteria']} cafeteria")
        cafeteria = Cafeteria.objects.get(name=record['cafeteria'])
        menu = Menu(
            cafeteria=cafeteria,
            name=record["name"],
            description=record["description"],
            menu_type=record["type"],
            price=record['price']
        )
        
        # read image file as binary using filepath to update menu image
        with open(f"{settings.BASE_DIR}/rms/static/images/menus/{record['image']}", "rb") as file:
            upload_file = SimpleUploadedFile(name=str(file.name), content=file.read())
            menu.image = upload_file
        menu.save()
        print(f"Successfully created {record['name']} menu record for {record['cafeteria']} cafeteria")