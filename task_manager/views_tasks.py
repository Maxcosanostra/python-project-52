from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

from .models import Task
from .filters import TaskFilter
from .forms_task import TaskForm


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    filterset_class = TaskFilter
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Задача успешно создана")
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task_list")

    def form_valid(self, form):
        messages.success(self.request, "Задача успешно изменена")
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("task_list")

    def test_func(self):
        return self.request.user.pk == self.get_object().author.pk

    def post(self, request, *args, **kwargs):
        messages.success(request, "Задача успешно удалена")
        return super().post(request, *args, **kwargs)
