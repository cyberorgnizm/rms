from django.views import generic
from . import models

class CafeteriaList(generic.ListView):
    model = models.Cafeteria
    template_name = "pages/restaurant-list.html"


class CafeteriaDetail(generic.DetailView):
    model = models.Cafeteria
    slug_field = 'slug'
    slug_url_kwarg = 'cafeteria_slug'
    template_name = "pages/restaurant-detail.html"


class CafeteriaMenuList(generic.ListView):
    model = models.Menu
    template_name = "pages/menu-list.html"
    

class CafeteriaMenuDetail(generic.DetailView):
    model = models.Cafeteria
    slug_field = 'slug'
    slug_url_kwarg = 'menu_slug'
    template_name = "pages/menu-detail.html"

