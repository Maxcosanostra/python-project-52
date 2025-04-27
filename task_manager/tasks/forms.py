from django import forms
from django.utils.translation import gettext_lazy as _

from ..tasks.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "assigned_to", "status", "labels"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["assigned_to"].label_from_instance = (
            lambda u: u.get_full_name() or u.username
        )
        self.fields["name"].label = _("Name")
        self.fields["description"].label = _("Description")
        self.fields["assigned_to"].label = _("Executor")
        self.fields["status"].label = _("Status")
        self.fields["labels"].label = _("Labels")

        self.fields["assigned_to"].widget.attrs["id"] = "id_executor"
