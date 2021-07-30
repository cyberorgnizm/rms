from django.views import generic

class HomeView(generic.TemplateView):
    template_name = "pages/index.html"


class AboutView(generic.TemplateView):
    template_name = "pages/about.html"
