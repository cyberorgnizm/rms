from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from phonenumber_field.formfields import PhoneNumberField
from . import models

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(
        attrs={'autofocus': True, 'class': 'form-control', 'placeholder': 'Email address here'}
        )
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password', 'class': 'form-control', 'placeholder': '**************'}),
    )
    remember_me = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input'}
        )
    )


class UserForm(forms.Form):
    first_name = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={
            'class': 'form-control form-control-sm'
        }
    ))
    last_name = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={
            'class': 'form-control form-control-sm'
        }
    ))
    avatar = forms.ImageField(label="", required=False, widget=forms.FileInput(
        attrs={
            'type': 'file',
            'class': 'filepond',
            'name': 'filepond',
            'accept': "image/png, image/jpeg, image/gif"
        }
    ))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control form-control-sm'
        }
    ))
    username = forms.CharField(max_length=255,  widget=forms.TextInput(
        attrs={
            'class': 'form-control form-control-sm'
        }
    ))
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(
        attrs={
            "placeholder": "**************",
            "class": "form-control form-control-sm"
        }
    ))
    confirm_password = forms.CharField(max_length=255, widget=forms.PasswordInput(
        attrs={
            "placeholder": "**************",
            "class": "form-control form-control-sm"
        }
    ))
    phone = PhoneNumberField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm'}
    ))
    gender = forms.CharField(
        max_length=255,
        widget=forms.Select(
            choices=models.Student.GENDER,
            attrs={'class': 'form-select form-select-sm'}
        )
    )

    def send_email(self):
        pass


class StudentForm(UserForm):
    field_order = [
        'avatar',
        'username',
        'password',
        'confirm_password',
        'photo',
        'first_name',
        'last_name',
        'email',
        'matric',
        'phone',
        'gender',
        'level',
        'department',
        'admission_year',
        'student_address'
    ]

    matric = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-sm'}
        )
    )

    level = forms.CharField(
        max_length=255,
        widget=forms.Select(
            choices=models.Student.COLLEGE_LEVELS,
            attrs={'class': 'form-select form-select-sm'}
        )
    )

    department = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-select form-select-sm'}
        )
    )

    admission_year = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'class': 'form-control form-control-sm', "type": "date"}
        )
    )

    student_address = forms.CharField(
        label="Address",
        widget=forms.Textarea(
            attrs={'class': 'form-control form-control-sm'}
        )
    )


class WorkerForm(UserForm):
    field_order = [
        'username',
        'password',
        'confirm_password',
        'photo',
        'first_name',
        'last_name',
        'email',
        'phone',
        'role',
    ]

    woker_role = forms.CharField(
        max_length=255,
        widget=forms.Select(
            choices=models.Worker.WORKER_ROLES
        )
    )
