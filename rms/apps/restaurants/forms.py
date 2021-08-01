from django import forms
from .models import RATING_CHOICES

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
    

