from django import forms
from django.contrib.auth.models import User

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "assigned_to", "status", "labels"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["assigned_to"].label_from_instance = (
            lambda obj: obj.get_full_name() or obj.username
        )
