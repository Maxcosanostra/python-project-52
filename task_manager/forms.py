from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task


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

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "assigned_to", "status", "labels"]
        labels = {
            "name": _("Имя"),
            "description": _("Описание"),
            "assigned_to": _("Исполнитель"),
            "status": _("Статус"),
            "labels": _("Метки"),
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": _("Имя")}),
            "description": forms.Textarea(attrs={"placeholder": _("Описание")}),
            "assigned_to": forms.Select(
                attrs={"aria-label": _("Исполнитель")}
            ),
            "status": forms.Select(
                attrs={"aria-label": _("Статус")}
            ),
            "labels": forms.SelectMultiple(
                attrs={"aria-label": _("Метки")}
            ),
        }