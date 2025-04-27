from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        label=_("First name"), max_length=30, required=False
    )
    last_name = forms.CharField(
        label=_("Last name"), max_length=150, required=False
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
        label=_("First name"), max_length=30, required=False
    )
    last_name = forms.CharField(
        label=_("Last name"), max_length=150, required=False
    )

    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
        required=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Confirm password"),
        widget=forms.PasswordInput,
        required=False,
        help_text=_("Please confirm your password."),
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
        )

    def clean(self):
        cleaned = super().clean()
        pwd1, pwd2 = cleaned.get("password1"), cleaned.get("password2")

        if pwd1 or pwd2:
            if pwd1 != pwd2:
                raise forms.ValidationError(_("Passwords do not match."))
            password_validation.validate_password(pwd1, self.instance)

        return cleaned
