from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView as BaseLoginView
from django.db import transaction
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse
from django.views import generic
from django.urls import reverse_lazy, reverse
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
        from rms.apps.orders.models import PurchaseOrder

        context = super().get_context_data(**kwargs)
        if self.request.user.is_student:
            user = self.model.objects.get(id=self.request.user.id)
            orders = PurchaseOrder.objects.filter(student=user.student)
            context["orders"] = orders
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(username=self.request.user.username)

class EditProfileView(generic.TemplateView):
    template_name = "registration/profile_settings.html"
    model = get_user_model()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['worker'] = get_user_model().objects.all()


    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        # check image upload
        upload = request.FILES.get('filepond', None)
        if upload:
            user = get_user_model().objects.get(username=request.user.username)
            user.avatar = upload
            user.save()
            return HttpResponse({"message": "success"})
            
        return HttpResponseRedirect(reverse('accounts:profile', kwargs={'username': self.request.user.username}))

