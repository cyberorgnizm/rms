from django.shortcuts import redirect
from django.views import generic
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from rms.apps.accounts.models import Student, Worker
from .models import Cafeteria, CafeteriaReview, Menu, MenuReview
from .forms import ReviewForm, MenuForm

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = MenuForm()
        return context


    def post(self, request, *args, **kwargs):
        # only restaurant manager can create menu
        if request.user.is_worker and request.user.worker.worker_role == "manager": 
            form = MenuForm(request.POST)
            if form.is_valid():
                    menu = Menu(
                        cafeteria=Cafeteria.objects.get(slug=kwargs["cafeteria_slug"]),
                        name=form.cleaned_data["name"],
                        price=form.cleaned_data["price"],
                        description=form.cleaned_data["description"],
                        menu_type=form.cleaned_data["menu_type"],
                        image=request.FILES["image"]
                    )
                    menu.save()
                    return redirect("restaurants:menu-list", cafeteria_slug=kwargs["cafeteria_slug"])
            else:
                messages.error(request, "Failed to add menu item")
                return redirect("restaurants:menu-list", cafeteria_slug=kwargs["cafeteria_slug"])
        else:
            messages.error(request, "Only authorized workers are required to add menu items")
            return redirect("restaurants:menu-list", cafeteria_slug=kwargs["cafeteria_slug"])
    

class CafeteriaMenuDetail(generic.DetailView):
    model = Menu
    slug_field = 'slug'
    slug_url_kwarg = 'menu_slug'
    template_name = "pages/menu-detail.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu = self.get_object()
        context["all_reviews"] = menu.reviews.all()
        if self.request.user.is_worker and self.request.user.worker.worker_role == "manager":
            menu = self.get_object()
            context["menu_form"] = MenuForm(data={
                "name": menu.name,
                "price":menu.price,
                "description": menu.description,
                "menu_type": menu.menu_type,
            })
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
                messages.success(request, "Review successfully submitted")
                return redirect("restaurants:menu-list", cafeteria_slug=kwargs["cafeteria_slug"])
            else:
                messages.error(request, "Failed to submit review")
                return redirect("restaurants:menu-detail", cafeteria_slug=kwargs["cafeteria_slug"], menu_slug=kwargs["menu_slug"])
        elif request.user.is_worker and request.user.worker.worker_role == "manager":
            worker = Worker.objects.get(user=request.user)
            form = MenuForm(request.POST)
            if form.is_valid():
                menu = self.get_object()
                menu.name = form.cleaned_data["name"]
                menu.price = form.cleaned_data["price"]
                menu.menu_type = form.cleaned_data["menu_type"]
                menu.description = form.cleaned_data["description"]
                menu.save()
                messages.success(request, "Successfully updated 1 menu")
                return redirect("restaurants:menu-list", cafeteria_slug=kwargs["cafeteria_slug"])
            else:
                return redirect("restaurants:menu-detail", cafeteria_slug=kwargs["cafeteria_slug"], menu_slug=kwargs["menu_slug"])


@login_required(login_url="/accounts/login")
def delete_menu(request, menu_slug, **kwargs):
    user = request.user
    if user.is_worker and user.worker.worker_role == 'manager':
        menu = get_object_or_404(Menu, slug=menu_slug)
        if menu.cafeteria == user.worker.cafeteria:
            menu.delete()
            return redirect("restaurants:menu-list", cafeteria_slug=kwargs["cafeteria_slug"])
        else:
            messages.error(request, "You cannot delete this menu because it doesn't belong to your cafeteria")
            return redirect("restaurants:menu-list", cafeteria_slug=kwargs["cafeteria_slug"])
    messages.error(request, "You are not authorized to remove this menu")
    return redirect("restaurants:menu-list", cafeteria_slug=kwargs["cafeteria_slug"])