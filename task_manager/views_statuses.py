from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from .models import Status, Task


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = "statuses/status_list.html"
    context_object_name = "statuses"


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    fields = ["name"]
    template_name = "statuses/status_form.html"
    success_url = reverse_lazy("status_list")

    def form_valid(self, form):
        messages.success(self.request, "Статус успешно создан")
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    fields = ["name"]
    template_name = "statuses/status_form.html"
    success_url = reverse_lazy("status_list")

    def form_valid(self, form):
        messages.success(self.request, "Статус успешно изменен")
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = "statuses/status_confirm_delete.html"
    success_url = reverse_lazy("status_list")

    def post(self, request, *args, **kwargs):
        status = self.get_object()
        if Task.objects.filter(status=status).exists():
            messages.error(
                request,
                "Невозможно удалить статус, потому что он используется",
            )
            return redirect("status_list")
        messages.success(request, "Статус успешно удален")
        return super().post(request, *args, **kwargs)
