from django import forms
import re


class ReportForm(forms.Form):

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Your Full Name"
            }
        )
    )

    location = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "id_location",
                "placeholder":  "Enter Location"
            }
        )
    )

    pincode = forms.CharField(
        max_length=6,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter 6 Digit Pincode"
            }
        )
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Describe the road damage or pothole..."
            }
        )
    )

    photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    def clean_pincode(self):

        pincode = self.cleaned_data["pincode"]

        if not re.match(r'^\d{6}$', pincode):
            raise forms.ValidationError(
                "Pincode must contain exactly 6 digits."
            )

        return pincode