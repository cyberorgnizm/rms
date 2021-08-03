from django import forms

class PurchaseOrderApproveForm(forms.Form):
    is_approved = forms.CharField(
        label="Mark all as complete and approve",
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input"}
        ),
        required=True
    )
    delivery_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"class": "form-control form-control-sm", "type": "date"}
        ),
        required=True
    )

class PurchaseOrderRejectForm(forms.Form):
    is_rejected = forms.CharField(
        label="Mark all as incomplete and cancel",
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input"}
        ),
        required=True
    )
    note = forms.CharField(
        label="Reason for rejecting order",
        widget=forms.Textarea(
            attrs={"class": "form-control form-control-sm", "rows": 3, "placeholder": "Reason for rejecting this order..."}
        ),
        required=True
    )