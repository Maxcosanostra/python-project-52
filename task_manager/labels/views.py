from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

import rollbar  # noqa:  E402 (может не быть в DEV-окружении)

from ..tasks.models import Task
from .forms import LabelForm
from .models import Label


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = "labels/label_list.html"
    context_object_name = "labels"


class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = "labels/label_form.html"
    success_url = reverse_lazy("label_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Метка успешно создана")

        # Отправляем сообщение в Rollbar, если включён
        if not settings.TESTING and settings.ROLLBAR.get("access_token"):
            rollbar.report_message(
                f"Label #{self.object.pk} («{self.object.name}») создана",
                "info",
                extra_data={"user_id": self.request.user.id},
            )
        return response


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = "labels/label_form.html"
    success_url = reverse_lazy("label_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Метка успешно изменена")

        if not settings.TESTING and settings.ROLLBAR.get("access_token"):
            rollbar.report_message(
                f"Label #{self.object.pk} («{self.object.name}») обновлена",
                "info",
                extra_data={"label_id": self.object.pk},
            )
        return response


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = "labels/label_confirm_delete.html"
    success_url = reverse_lazy("label_list")

    def post(self, request, *args, **kwargs):
        label = self.get_object()

        # запрет, если метка привязана к задачам
        if Task.objects.filter(labels=label).exists():
            messages.error(
                request,
                "Невозможно удалить метку, потому что она используется",
            )
            if not settings.TESTING and settings.ROLLBAR.get("access_token"):
                rollbar.report_message(
                    f"Attempted to delete Label "
                    f"#{label.pk} («{label.name}») but it is in use",
                    "warning",
                    extra_data={"label_id": label.pk},
                )
            return redirect("label_list")

        messages.success(request, "Метка успешно удалена")
        if not settings.TESTING and settings.ROLLBAR.get("access_token"):
            rollbar.report_message(
                f"Label #{label.pk} («{label.name}») удалена",
                "info",
                extra_data={"label_id": label.pk},
            )
        return super().post(request, *args, **kwargs)
