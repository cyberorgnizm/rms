"""rms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.utils.translation import gettext_lazy
from django.conf import settings
from django.views.generic.base import TemplateView


admin.site.site_title = gettext_lazy("RMS site admin")
admin.site.site_header = gettext_lazy("Restaurant Management System (RMS) administation")
admin.site.enable_nav_sidebar = False
admin.site.empty_value_display = "N/A"

urlpatterns = [
    path('', TemplateView.as_view(template_name="pages/index.html"), name='home'),
    path('about', TemplateView.as_view(template_name="pages/about.html"), name='about'),
    path("accounts/", include("rms.apps.accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("restaurants/", include("rms.apps.restaurants.urls")),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    # serve static files
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # server files uploaded
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
