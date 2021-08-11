from django.urls import path
from . import views

app_name='accounts'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('student/signup/', views.StudentRegistrationView.as_view(), name='signup_student'),
    path('lecturer/signup/', views.LecturerRegistrationView.as_view(), name='signup_lecturer'),
    path('profile/<slug:username>/', views.ProfileView.as_view(), name='profile'),
    path('profile/<slug:username>/settings', views.EditProfileView.as_view(), name='setting'),
]