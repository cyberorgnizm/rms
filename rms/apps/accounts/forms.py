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
            'class': 'form-control'
        }
    ))
    last_name = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    avatar = forms.ImageField(label="Picture", required=False, widget=forms.FileInput(
        attrs={
            'class': 'filepond',
            'accept': "image/png, image/jpeg, image/gif"
        }
    ))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control'
        }
    ))
    username = forms.CharField(max_length=255,  widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(
        attrs={
            "placeholder": "**************",
            "class": "form-control"
        }
    ))
    confirm_password = forms.CharField(max_length=255, widget=forms.PasswordInput(
        attrs={
            "placeholder": "**************",
            "class": "form-control"
        }
    ))
    phone = PhoneNumberField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))
    gender = forms.CharField(
        max_length=255,
        widget=forms.Select(
            choices=models.Student.GENDER,
            attrs={'class': 'form-select'}
        )
    )

    def send_email(self):
        pass


class StudentForm(UserForm):
    field_order = [
        'username',
        'password',
        'confirm_password',
        'photo',
        'first_name',
        'last_name',
        'email',
        'matriculation_number',
        'phone',
        'gender',
        'level',
        'department',
        'admission_year'
    ]

    matriculation_number = forms.CharField()

    level = forms.CharField(
        max_length=255,
        widget=forms.Select(
            choices=models.Student.COLLEGE_LEVELS,
            attrs={'class': 'form-select'}
        )
    )

    department = forms.CharField(
        max_length=255,
        widget=forms.Select(
            attrs={'class': 'form-select'}
        )
    )

    admission_year = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'class': 'form-control'}
        )
    )

    address = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control'}
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

    role = forms.CharField(
        max_length=255,
        widget=forms.Select(
            choices=models.Worker.WORKER_ROLES
        )
    )
