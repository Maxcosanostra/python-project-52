from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Status, Task


class TaskCrudTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser",
                                             password="StrongPassword123")
        self.client.login(username="testuser", password="StrongPassword123")

        self.status = Status.objects.create(name="New")
        self.task = Task.objects.create(
            name="Test Task",
            description="Task description",
            status=self.status,
            author=self.user
        )

    def test_task_list_view(self):
        response = self.client.get(reverse("task_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Task")

    def test_task_detail_view(self):
        response = self.client.get(reverse("task_detail", args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Task description")

    def test_task_create_view(self):
        response = self.client.post(reverse("task_create"), {
            "name": "New Task",
            "description": "New task description",
            "status": self.status.pk
        })
        self.assertRedirects(response, reverse("task_list"))
        self.assertTrue(Task.objects.filter(name="New Task").exists())

    def test_task_update_view(self):
        response = self.client.post(
            reverse("task_update", args=[self.task.pk]), {
                "name": "Updated Task",
                "description": "Updated description",
                "status": self.status.pk
            })
        self.assertRedirects(response, reverse("task_list"))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Updated Task")

    def test_task_delete_view(self):
        response = self.client.post(
            reverse("task_delete", args=[self.task.pk]))
        self.assertRedirects(response, reverse("task_list"))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_task_delete_by_non_author(self):
        other_user = User.objects.create_user(username="other",
                                              password="OtherPassword123")
        self.client.logout()
        self.client.login(username="other", password="OtherPassword123")
        response = self.client.post(
            reverse("task_delete", args=[self.task.pk]))
        self.assertEqual(response.status_code, 403)
