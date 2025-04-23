from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "assigned_to", "status", "labels"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["assigned_to"].label_from_instance = (
            lambda u: u.get_full_name() or u.username
        )
        self.fields["name"].label = _("Имя")
        self.fields["description"].label = _("Описание")
        self.fields["assigned_to"].label = _("Исполнитель")
        self.fields["status"].label = _("Статус")
        self.fields["labels"].label = _("Метки")

        self.fields["assigned_to"].widget.attrs["id"] = "id_executor"
