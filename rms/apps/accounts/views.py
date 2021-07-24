from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView as BaseLoginView
from django.db import transaction
from django.http import response
from django.views import generic
from django.urls import reverse_lazy
from . import forms, models


class RegistrationView(generic.FormView):
    form_class = forms.UserForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"
    
    @transaction.atomic
    def form_valid(self, form):
        response = super().form_valid(form)
        form.cleaned_data.pop('confirm_password')
        form.cleaned_data.pop('gender')
        user = get_user_model().objects.create(**form.cleaned_data)
        user.set_password(form.cleaned_data.get('password'))
        user.save()
        return response


class LoginView(BaseLoginView):
    form_class = forms.LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data['remember_me']  # get remember me data from cleaned_data of form
        if not remember_me:
             self.request.session.set_expiry(0)  # if remember me is set
             self.request.session.modified = True
        return super().form_valid(form)

class ProfileView(LoginRequiredMixin, generic.DetailView):
    login_url = reverse_lazy('accounts:login')
    redirect_field_name = 'redirect_to'
    model = models.User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = "registration/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(username=self.request.user.username)

class EditProfileView(generic.TemplateView):
    template_name = "registration/profile_settings.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['worker'] = get_user_model().objects.all()

