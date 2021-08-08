from django import forms
from .models import RATING_CHOICES, Menu

class ReviewForm(forms.Form):
    rating = forms.CharField(
        widget=forms.Select(
            attrs={
                "class": "form-select form-select-md"
            },
            choices=RATING_CHOICES
        )
    )

    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control mb-3"
            }
        )
    )
    

class MenuForm(forms.Form):
    field_order = [
        'name',
        'price',
        'menu_type',
        'description'
    ]


    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-sm mb-3"
            }
        )
    )
    price = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-sm mb-3",
                "type": "number"
            }
        )
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control form-control-sm mb-3",
                "rows": 3
            }
        )
    )
    menu_type = forms.CharField(
        widget=forms.Select(
            choices=Menu.MENU_TYPES,
            attrs={
                "class": "form-select form-select-sm mb-3"
            }
        )
    )