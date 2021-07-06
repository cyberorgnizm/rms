from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "pages/index.html"


class AboutView(TemplateView):
    template_name = "pages/about.html"
