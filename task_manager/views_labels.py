import rollbar
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from .models import Label, Task

class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = "labels/label_list.html"
    context_object_name = "labels"

class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    fields = ['name']
    template_name = "labels/label_form.html"
    success_url = reverse_lazy("label_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Метка успешно создана")
        # Отправка события в Rollbar для проверки интеграции
        rollbar.report_message(
            f"Label #{self.object.pk} («{self.object.name}») создана",
            'info',
            extra_data={
                'user_id': self.request.user.id,
                'label_name': self.object.name,
            }
        )
        return response

class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    fields = ['name']
    template_name = "labels/label_form.html"
    success_url = reverse_lazy("label_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Метка успешно обновлена")
        return response

class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = "labels/label_confirm_delete.html"
    success_url = reverse_lazy("label_list")

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        label = self.get_object()
        # Если метка используется в задаче — отказываем и логируем в Rollbar
        if Task.objects.filter(labels=label).exists():
            messages.error(request, "Невозможно удалить метку, потому что она используется")
            rollbar.report_message(
                f"Attempted to delete Label #{label.pk} («{label.name}») but it is in use",
                'warning',
                extra_data={'label_id': label.pk}
            )
            return redirect("label_list")
        messages.success(request, "Метка успешно удалена")
        return super().delete(request, *args, **kwargs)
