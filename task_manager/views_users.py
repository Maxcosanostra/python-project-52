from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


class UserListView(ListView):
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"


class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request, _("Registration successful. Please log in."))
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserChangeForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("user_list")

    def test_func(self):
        return self.request.user.pk == self.get_object().pk

    def form_valid(self, form):
        messages.success(self.request, _("Profile updated successfully."))
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = "users/user_confirm_delete.html"
    success_url = reverse_lazy("user_list")

    def test_func(self):
        return self.request.user.pk == self.get_object().pk

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _("Your account has been deleted."))
        return super().delete(request, *args, **kwargs)


class LoginView(AuthLoginView):
    template_name = "users/login.html"

    def form_valid(self, form):
        messages.success(self.request, _("You are logged in."))
        return super().form_valid(form)


class LogoutView(AuthLogoutView):
    next_page = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        messages.success(request, _("You have been logged out."))
        return super().post(request, *args, **kwargs)
