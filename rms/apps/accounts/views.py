from django.views import generic

class ProfileView(generic.TemplateView):
    template_name = "registration/profile.html"