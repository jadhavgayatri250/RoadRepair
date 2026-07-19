from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter Password"
        })
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Confirm Password"
        })
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]

        widgets = {
            "username": forms.TextInput(attrs={
                "placeholder": "Enter Username"
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "Enter Email"
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        username = cleaned_data.get("username")

        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")

        email = cleaned_data.get("email")

        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")

        return cleaned_data