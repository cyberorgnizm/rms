from django.urls import path
from . import views

app_name='accounts'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.RegistrationView.as_view(), name='signup'),
    path('profile/<slug:username>/', views.ProfileView.as_view(), name='profile'),
    path('profile/<slug:username>/settings', views.EditProfileView.as_view(), name='setting'),
]