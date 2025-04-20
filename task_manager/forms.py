from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        label=_("First name"),
        max_length=30,
        required=False,
    )
    last_name = forms.CharField(
        label=_("Last name"),
        max_length=150,
        required=False,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
        )


class CustomUserChangeForm(forms.ModelForm):
    first_name = forms.CharField(
        label=_("First name"),
        max_length=30,
        required=False,
    )
    last_name = forms.CharField(
        label=_("Last name"),
        max_length=150,
        required=False,
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
        )
