import django_filters
from django import forms
from django.contrib.auth.models import User
from .models import Task


class TaskFilter(django_filters.FilterSet):
    my_tasks = django_filters.BooleanFilter(
        method="filter_my_tasks",
        widget=forms.CheckboxInput,
        label="Только свои задачи",
    )
    assigned_to = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label="Исполнитель",
    )

    class Meta:
        model = Task
        fields = {
            "status": ["exact"],
            "assigned_to": ["exact"],
            "labels": ["exact"],
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get("request", None)
        super().__init__(*args, **kwargs)

        self.filters["status"].label = "Статус"
        self.filters["labels"].label = "Метка"

        self.filters["assigned_to"].field.label_from_instance = (
            lambda u: u.get_full_name() or u.username
        )

    def filter_my_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
