from django.views import generic
from django.db.models import F, Avg
from .apps.restaurants.models import Cafeteria, Menu

class HomeView(generic.TemplateView):
    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # most liked cafeterias
        cafeteria_rating_filter = Cafeteria.objects.all().filter(reviews__rating__gte=3)
        distinct_cafeteria = cafeteria_rating_filter.distinct()[:3]
        context["top_cafeterias"] = distinct_cafeteria.annotate(avg_reviews=Avg(F('reviews__rating')))

        # most liked menus
        menu_rating_filter = Menu.objects.all().filter(reviews__rating__gte=3)
        distinct_menu = menu_rating_filter.distinct()[:3]
        context["top_menus"] = distinct_menu.annotate(avg_reviews=Avg(F('reviews__rating')))
        return context

class AboutView(generic.TemplateView):
    template_name = "pages/about.html"
