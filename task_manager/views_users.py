from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import (
    LoginView as AuthLoginView,
    LogoutView as AuthLogoutView,
    PasswordChangeView,
)
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Task


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

    def test_func(self):
        return self.request.user.pk == self.get_object().pk

    def form_valid(self, form):
        messages.success(
            self.request,
            _("Пользователь успешно изменен"),
        )
        return super().form_valid(form)

    # гарантируем, что чужой профиль не редактируется
    def dispatch(self, request, *args, **kwargs):
        if request.user.pk != kwargs["pk"]:
            return redirect("user_list")
        return super().dispatch(request, *args, **kwargs)


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = "users/password_change_form.html"
    success_url = reverse_lazy("user_list")

    def form_valid(self, form):
        messages.success(
            self.request,
            _("Пароль успешно изменен"),
        )
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "users/user_confirm_delete.html"
    success_url = reverse_lazy("user_list")

    def _cannot_delete(self, user):
        is_foreign = self.request.user.pk != user.pk
        has_authored = Task.objects.filter(author=user).exists()
        has_assigned = Task.objects.filter(assigned_to=user).exists()
        return is_foreign or has_authored or has_assigned

    # — GET —
    def get(self, request, *args, **kwargs):
        user = self.get_object()
        if self._cannot_delete(user):
            messages.error(
                request,
                _("Невозможно удалить пользователя: есть связанные задачи."),
            )
            return redirect("user_list")
        return super().get(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        if self._cannot_delete(user):
            messages.error(
                request,
                _("Невозможно удалить пользователя: есть связанные задачи."),
            )
            return redirect("user_list")
        messages.success(request, _("Пользователь успешно удален"))
        return super().delete(request, *args, **kwargs)



class LoginView(AuthLoginView):
    template_name = "users/login.html"

    def form_valid(self, form):
        messages.success(
            self.request,
            _("You are logged in."),
        )
        return super().form_valid(form)


class LogoutView(AuthLogoutView):
    next_page = reverse_lazy("index")

    def post(self, request, *args, **kwargs):
        messages.info(
            request,
            _("You have been logged out."),
        )
        return super().post(request, *args, **kwargs)
