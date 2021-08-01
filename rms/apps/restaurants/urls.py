from django.urls import path
from .views import CafeteriaList, CafeteriaDetail, CafeteriaMenuList, CafeteriaMenuDetail


app_name = "restaurants"

urlpatterns = [
    path('', CafeteriaList.as_view(), name="cafeterias"),
    path('<slug:cafeteria_slug>/', CafeteriaDetail.as_view(), name='cafeteria-detail'),
    path('<slug:cafeteria_slug>/menu/', CafeteriaMenuList.as_view(), name='menu-list'),
    path('<slug:cafeteria_slug>/menu/<slug:menu_slug>/', CafeteriaMenuDetail.as_view(), name='menu-detail'),
]