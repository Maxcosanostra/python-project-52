import django_filters
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from ..tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    my_tasks = django_filters.BooleanFilter(
        method="filter_my_tasks",
        widget=forms.CheckboxInput,
        label=_("Only my tasks"),
    )
    assigned_to = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label=_("Executor"),
    )

    class Meta:
        model = Task
        fields = {
            "status": ["exact"],
            "assigned_to": ["exact"],
            "labels": ["exact"],
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get("request")
        super().__init__(*args, **kwargs)

        self.filters["status"].label = _("Status")
        self.filters["labels"].label = _("Label")
        self.filters["assigned_to"].field.label_from_instance = (
            lambda u: u.get_full_name() or u.username
        )

    def filter_my_tasks(self, queryset, name, value):
        if value and self.request:
            return queryset.filter(author=self.request.user)
        return queryset
