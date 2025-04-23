from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView as AuthLoginView,
    LogoutView as AuthLogoutView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Task

User = get_user_model()


class UserListView(ListView):
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"


class UserCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(
            self.request,
            _("Registration successful. Please log in."),
        )
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("user_list")

    def dispatch(self, request, *args, **kwargs):
        if request.user.pk != kwargs["pk"]:
            messages.error(request, _("У вас нет прав для изменения"))
            return redirect("user_list")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, _("Пользователь успешно изменен"))
        return super().form_valid(form)


class UserPasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = PasswordChangeForm
    template_name = "users/password_change_form.html"
    success_url = reverse_lazy("user_list")
    success_message = _("Пароль успешно изменен")

    def get_object(self):
        return self.request.user


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "users/user_confirm_delete.html"
    success_url = reverse_lazy("user_list")

    def _has_related_tasks(self, user):
        return (
            Task.objects.filter(author=user).exists()
            or Task.objects.filter(assigned_to=user).exists()
        )

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.user.pk != self.object.pk:
            messages.error(request, _("У вас нет прав для изменения"))
            return redirect("user_list")

        if self._has_related_tasks(self.object):
            messages.error(
                request,
                _("Невозможно удалить пользователя: есть связанные задачи."),
            )
            return redirect("user_list")

        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        messages.success(request, _("Пользователь успешно удален"))

        self.object.delete()

        return redirect(self.get_success_url())


class LoginView(AuthLoginView):
    template_name = "users/login.html"

    def form_valid(self, form):
        messages.success(self.request, _("You are logged in."))
        return super().form_valid(form)


class LogoutView(AuthLogoutView):
    next_page = reverse_lazy("index")

    def post(self, request, *args, **kwargs):
        messages.info(self.request, _("You have been logged out."))
        return super().post(request, *args, **kwargs)
