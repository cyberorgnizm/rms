from django.urls import path
from . import views

app_name = "restaurants"

urlpatterns = [
    path('', views.CafeteriaList.as_view(), name="cafeterias"),
    path('<slug:cafeteria_slug>/', views.CafeteriaDetail.as_view(), name='cafeteria-detail'),
]