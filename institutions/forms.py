from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Login Form: Handles user authentication input
class LoginForm(forms.Form):

    # Username input field
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Username"
        })
    )

    # Password input field
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Password"
        })
    )


# User Registration Form: Extends Django's built-in UserCreationForm
class RegisterForm(UserCreationForm):

    # Custom email field with styling
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Email"
        })
    )

    class Meta:
        model = User

        # Fields displayed in the registration form
        fields = [
            "username",
            "email",
            "password1",
            "password2"
        ]

    # Add consistent styling to all form fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Apply Bootstrap/custom CSS class
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control"
            })