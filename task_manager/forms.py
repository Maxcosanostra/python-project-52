from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Task


# -------------------- пользователи -------------------- #
class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации."""

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
    """Форма редактирования профиля + смена пароля."""

    # личные данные
    first_name = forms.CharField(
        label=_("First name"), max_length=30, required=False
    )
    last_name = forms.CharField(
        label=_("Last name"), max_length=150, required=False
    )

    # смена пароля
    password1 = forms.CharField(
        label=_("Пароль"),
        widget=forms.PasswordInput,
        required=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Подтверждение пароля"),
        widget=forms.PasswordInput,
        required=False,
        help_text=_("Для подтверждения введите, пожалуйста, пароль ещё раз."),
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

    # ---------- валидация паролей ---------- #
    def clean(self):
        cleaned = super().clean()
        pwd1 = cleaned.get("password1")
        pwd2 = cleaned.get("password2")

        if pwd1 or pwd2:  # меняем пароль только если что-то введено
            if pwd1 != pwd2:
                raise forms.ValidationError(_("Пароли не совпадают."))

            # прогоняем сквозь стандартные валидаторы
            password_validation.validate_password(pwd1, self.instance)

        return cleaned


# -------------------- задачи -------------------- #
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
            "description": forms.Textarea(
                attrs={"placeholder": _("Описание")}
            ),
            "assigned_to": forms.Select(
                attrs={"aria-label": _("Исполнитель")}
            ),
            "status": forms.Select(attrs={"aria-label": _("Статус")}),
            "labels": forms.SelectMultiple(attrs={"aria-label": _("Метки")}),
        }
