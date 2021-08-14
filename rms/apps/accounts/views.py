import uuid
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy, reverse
from . import forms, models


class StudentRegistrationView(generic.FormView):
    form_class = forms.StudentForm
    success_url = reverse_lazy('login')
    template_name = "registration/student-signup.html"

    @transaction.atomic
    def form_valid(self, form):
        response = super().form_valid(form)
        # Create user to be associated with student
        user = get_user_model().objects.create(
            username=form.cleaned_data["username"],
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            email=form.cleaned_data["email"],
            gender=form.cleaned_data["gender"],
            phone=form.cleaned_data["phone"],
            is_student=True
        )
        user.set_password(form.cleaned_data.get('password'))
        user.save()

        models.Student.objects.create(
            user=user,
            level=form.cleaned_data["level"],
            matric=form.cleaned_data["matric"],
            department=form.cleaned_data["department"],
            admission_year=form.cleaned_data["admission_year"],
            student_address=form.cleaned_data["student_address"]
        )

        return response



class LecturerRegistrationView(generic.FormView):
    form_class = forms.LecturerForm
    success_url = reverse_lazy('login')
    template_name = "registration/lecturer-signup.html"
    
    @transaction.atomic
    def form_valid(self, form):
        response = super().form_valid(form)
        # Create user to be associated with student
        user = get_user_model().objects.create(
            username=form.cleaned_data["username"],
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            email=form.cleaned_data["email"],
            gender=form.cleaned_data["gender"],
            phone=form.cleaned_data["phone"],
            is_lecturer=True
        )
        user.set_password(form.cleaned_data.get('password'))
        user.save()

        models.Lecturer.objects.create(
            user=user,
            staff_id=str(uuid.uuid4()),
            department=form.cleaned_data["department"],
            lecturer_address=form.cleaned_data["lecturer_address"]
        )

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
        if self.request.user.is_student or  self.request.user.is_lecturer:
            user = self.model.objects.get(id=self.request.user.id)
            orders = PurchaseOrder.objects.filter(user=user)
            context["orders"] = orders
        elif self.request.user.is_worker:
            user = self.model.objects.get(id=self.request.user.id)
            orders = PurchaseOrder.objects.filter(cafeteria=user.worker.cafeteria)
            context["orders"] = orders
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(username=self.request.user.username)

class EditProfileView(LoginRequiredMixin, generic.TemplateView):
    login_url = reverse_lazy('accounts:login')
    redirect_field_name = 'redirect_to'
    template_name = "registration/profile_settings.html"
    model = get_user_model()

    def get_user_data(self):
        data = dict()
        user = self.request.user
        # TODO: this code is a mess
        data["first_name"] = user.first_name
        data["last_name"] = user.last_name
        data["email"] = user.email
        data["username"] = user.username
        data["phone"] = user.phone
        data["gender"] = user.gender
        return data


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['worker'] = get_user_model().objects.all()
        
        data = self.get_user_data()

        if self.request.user.is_student:
            student = self.request.user.student
            # TODO: so is this one
            data["matric"] = student.matric
            data["level"] = student.level
            data["department"] = student.department
            data["student_address"] = student.student_address
            context["form"] = forms.StudentForm(data)
        elif self.request.user.is_lecturer:
            lecturer = self.request.user.lecturer
            data["department"] = lecturer.department
            data["lecturer_address"] = lecturer.lecturer_address
            context["form"] = forms.LecturerForm(data)
        elif self.request.user.is_worker:
            worker = self.request.user.worker
            data["worker_role"] = worker.worker_role
            context["form"] = forms.WorkerForm(data)
        return context


    def post(self, request, *args, **kwargs):
        user = get_user_model().objects.get(id=self.request.user.id)
        if user.is_worker:
            form = forms.WorkerForm(request.POST)
            if form.is_valid():
                # FIXME: I should probably do something about this
                user.username=form.cleaned_data["username"]
                user.first_name=form.cleaned_data["first_name"]
                user.last_name=form.cleaned_data["last_name"]
                user.email=form.cleaned_data["email"]
                user.gender=form.cleaned_data["gender"]
                user.phone=form.cleaned_data["phone"]
                user.save()
                user.worker.worker_role=form.cleaned_data["worker_role"]
                user.worker.save()
            else:
                messages.error(request, form.errors)
                return HttpResponseRedirect(reverse('accounts:setting', kwargs={'username': user.username}))
        elif user.is_student or user.is_lecturer:
            if user.is_student:
                form = forms.StudentForm(request.POST)
                if form.is_valid():
                    # FIXME: seriously...
                    user.username=form.cleaned_data["username"]
                    user.first_name=form.cleaned_data["first_name"]
                    user.last_name=form.cleaned_data["last_name"]
                    user.email=form.cleaned_data["email"]
                    user.gender=form.cleaned_data["gender"]
                    user.phone=form.cleaned_data["phone"]
                    user.save()
                    user.student.matric=form.cleaned_data["matric"]
                    user.student.level=form.cleaned_data["level"]
                    user.student.department=form.cleaned_data["department"]
                    user.student.admission_year=form.cleaned_data["admission_year"]
                    user.student.student_address=form.cleaned_data["student_address"]
                    user.student.save()
                else:
                    messages.error(request, form.errors)
                    return HttpResponseRedirect(reverse('accounts:setting', kwargs={'username': user.username}))
            else:
                form = forms.LecturerForm(request.POST)
                if form.is_valid():
                    # FIXME: seriously...
                    user.username=form.cleaned_data["username"]
                    user.first_name=form.cleaned_data["first_name"]
                    user.last_name=form.cleaned_data["last_name"]
                    user.email=form.cleaned_data["email"]
                    user.gender=form.cleaned_data["gender"]
                    user.phone=form.cleaned_data["phone"]
                    user.save()
                    user.lecturer.department=form.cleaned_data["department"]
                    user.lecturer.lecturer_address=form.cleaned_data["lecturer_address"]
                    user.lecturer.save()
                else:
                    messages.error(request, form.errors)
                    return HttpResponseRedirect(reverse('accounts:setting', kwargs={'username': user.username}))
        # check image upload
        upload = request.FILES.get('filepond', None)
        if upload:
            user = get_user_model().objects.get(username=user.username)
            user.avatar = upload
            user.save()
            return HttpResponseRedirect(reverse('accounts:setting', kwargs={'username': user.username}))
            
        return HttpResponseRedirect(reverse('accounts:profile', kwargs={'username': user.username}))

