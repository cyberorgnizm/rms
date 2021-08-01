from django.shortcuts import redirect
from django.views import generic
from rms.apps.accounts.models import Student
from .models import Cafeteria, CafeteriaReview, Menu, MenuReview
from .forms import ReviewForm

class CafeteriaList(generic.ListView):
    model = Cafeteria
    template_name = "pages/restaurant-list.html"


class CafeteriaDetail(generic.DetailView):
    model = Cafeteria
    slug_field = 'slug'
    slug_url_kwarg = 'cafeteria_slug'
    template_name = "pages/restaurant-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cafeteria = self.get_object()
        context["reviews"] = cafeteria.reviews.all()
        context["manager"] = cafeteria.workers.get(worker_role='manager')
        try:
            review = cafeteria.reviews.get(reviewer__user=self.request.user)
            context["review"] = review
        except:
            context["form"] = ReviewForm(self.request.POST)
        return context

    
    def post(self, request, *args, **kwargs):
        if request.user.is_student:
            student = Student.objects.get(user=request.user)
            form = ReviewForm(request.POST)
            if form.is_valid():
                CafeteriaReview.objects.create(
                    cafeteria=self.get_object(),
                    reviewer=student,
                    rating=form.cleaned_data["rating"],
                    comment=form.cleaned_data["comment"]
                )
                return redirect("restaurants:cafeterias")
            else:
                return redirect("restaurants:cafeteria-detail", cafeteria_slug=kwargs["cafeteria_slug"])



class CafeteriaMenuList(generic.ListView):
    model = Menu
    template_name = "pages/menu-list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        cafeteria_slug = self.kwargs["cafeteria_slug"]
        queryset = queryset.filter(cafeteria__slug=cafeteria_slug)
        return queryset
    

class CafeteriaMenuDetail(generic.DetailView):
    model = Menu
    slug_field = 'slug'
    slug_url_kwarg = 'menu_slug'
    template_name = "pages/menu-detail.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu = self.get_object()
        context["all_reviews"] = menu.reviews.all()
        try:
            review = menu.reviews.get(reviewer__user=self.request.user)
            context["review"] = review
        except:
            context["form"] = ReviewForm(self.request.POST)
        finally:
            return context

    
    def post(self, request, *args, **kwargs):
        if request.user.is_student:
            student = Student.objects.get(user=request.user)
            form = ReviewForm(request.POST)
            if form.is_valid():
                MenuReview.objects.create(
                    menu=self.get_object(),
                    reviewer=student,
                    rating=form.cleaned_data["rating"],
                    comment=form.cleaned_data["comment"]
                )
                return redirect("restaurants:menu-list", cafeteria_slug=kwargs["cafeteria_slug"])
            else:
                return redirect("restaurants:menu-detail", cafeteria_slug=kwargs["cafeteria_slug"], menu_slug=kwargs["menu_slug"])

