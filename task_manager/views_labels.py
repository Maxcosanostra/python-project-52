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
        messages.success(self.request, "Label created successfully.")
        return super().form_valid(form)

class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    fields = ['name']
    template_name = "labels/label_form.html"
    success_url = reverse_lazy("label_list")

    def form_valid(self, form):
        messages.success(self.request, "Label updated successfully.")
        return super().form_valid(form)

class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = "labels/label_confirm_delete.html"
    success_url = reverse_lazy("label_list")

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        label = self.get_object()
        if Task.objects.filter(labels=label).exists():
            messages.error(request, "Cannot delete label because it is associated with one or more tasks.")
            return redirect("label_list")
        messages.success(request, "Label deleted successfully.")
        return super().delete(request, *args, **kwargs)