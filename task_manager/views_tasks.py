from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Task

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['name', 'description', 'assigned_to', 'status']
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Task created successfully.")
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['name', 'description', 'assigned_to', 'status']
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task_list")

    def form_valid(self, form):
        messages.success(self.request, "Task updated successfully.")
        return super().form_valid(form)

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("task_list")

    def test_func(self):
        return self.request.user.pk == self.get_object().author.pk

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Task deleted successfully.")
        return super().delete(request, *args, **kwargs)
