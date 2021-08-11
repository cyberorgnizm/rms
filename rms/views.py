from django.views import generic
from django.db.models import F, Avg
from .apps.restaurants.models import Cafeteria

class HomeView(generic.TemplateView):
    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cafeteria_rating_filter = Cafeteria.objects.all().filter(reviews__rating__gte=3)
        distinct_cafeteria = cafeteria_rating_filter.distinct()
        context["top_cafeterias"] = distinct_cafeteria.order_by('name').annotate(avg_reviews=Avg(F('reviews__rating')))
        return context

class AboutView(generic.TemplateView):
    template_name = "pages/about.html"
