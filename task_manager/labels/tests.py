from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Label
from ..statuses.models import Status
from ..tasks.models import Task


class LabelCrudTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="StrongPassword123"
        )
        self.client.login(username="testuser", password="StrongPassword123")
        self.status = Status.objects.create(name="New")
        self.label = Label.objects.create(name="Bug")

    def test_label_list_view(self):
        response = self.client.get(reverse("label_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bug")

    def test_label_create_view(self):
        response = self.client.post(
            reverse("label_create"), {"name": "Feature"}
        )
        self.assertRedirects(response, reverse("label_list"))
        self.assertTrue(Label.objects.filter(name="Feature").exists())

    def test_label_update_view(self):
        response = self.client.post(
            reverse("label_update", args=[self.label.pk]),
            {"name": "Critical Bug"},
        )
        self.assertRedirects(response, reverse("label_list"))
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, "Critical Bug")

    def test_label_delete_view(self):
        task = Task.objects.create(
            name="Test Task",
            description="Task description",
            status=self.status,
            author=self.user,
        )
        task.labels.add(self.label)
        response = self.client.post(
            reverse("label_delete", args=[self.label.pk])
        )
        self.assertRedirects(response, reverse("label_list"))
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())

        self.label.tasks.clear()
        response = self.client.post(
            reverse("label_delete", args=[self.label.pk])
        )
        self.assertRedirects(response, reverse("label_list"))
        self.assertFalse(Label.objects.filter(pk=self.label.pk).exists())
