from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task, Status, Label


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
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=True,
        label=_("Статус"),
        empty_label=_("Статус"),  # ← пустая опция с текстом "Статус"
        widget=forms.Select(attrs={"aria-label": _("Статус")}),
    )
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label=_("Исполнитель"),
        empty_label=_("Исполнитель"),  # ← пустая опция с текстом "Исполнитель"
        widget=forms.Select(attrs={"aria-label": _("Исполнитель")}),
    )
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        required=False,
        label=_("Метки"),
        widget=forms.SelectMultiple(attrs={"aria-label": _("Метки")}),
    )

    class Meta:
        model = Task
        fields = ["name", "description", "assigned_to", "status", "labels"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": _("Имя")}),
            "description": forms.Textarea(attrs={"placeholder": _("Описание")}),
        }
