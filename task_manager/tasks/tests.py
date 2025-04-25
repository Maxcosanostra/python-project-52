from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Task
from ..statuses.models import Status
from ..labels.models import Label


class TaskCrudTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="StrongPassword123"
        )
        self.client.login(username="testuser", password="StrongPassword123")
        self.status = Status.objects.create(name="New")
        self.task = Task.objects.create(
            name="Test Task",
            description="Task description",
            status=self.status,
            author=self.user,
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
        response = self.client.post(
            reverse("task_create"),
            {
                "name": "New Task",
                "description": "New task description",
                "status": self.status.pk,
            },
        )
        self.assertRedirects(response, reverse("task_list"))
        self.assertTrue(Task.objects.filter(name="New Task").exists())

    def test_task_update_view(self):
        response = self.client.post(
            reverse("task_update", args=[self.task.pk]),
            {
                "name": "Updated Task",
                "description": "Updated description",
                "status": self.status.pk,
            },
        )
        self.assertRedirects(response, reverse("task_list"))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Updated Task")

    def test_task_delete_view(self):
        response = self.client.post(
            reverse("task_delete", args=[self.task.pk])
        )
        self.assertRedirects(response, reverse("task_list"))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_task_delete_by_non_author(self):
        other = User.objects.create_user(
            username="other", password="OtherPassword123"
        )
        self.client.logout()
        self.client.login(username="other", password="OtherPassword123")

        url = reverse("task_delete", args=[self.task.pk])
        response = self.client.post(url, follow=True)

        self.assertRedirects(response, reverse("task_list"))
        self.assertContains(
            response,
            "Задачу может удалить только ее автор",
        )


class TaskFilterTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="StrongPass123"
        )
        self.user2 = User.objects.create_user(
            username="otheruser", password="OtherPass123"
        )
        self.status_new = Status.objects.create(name="New")
        self.status_in_progress = Status.objects.create(name="In Progress")
        self.label_bug = Label.objects.create(name="Bug")
        self.label_feature = Label.objects.create(name="Feature")

        self.task1 = Task.objects.create(
            name="Task 1",
            description="Description 1",
            status=self.status_new,
            author=self.user,
        )
        self.task1.labels.add(self.label_bug)

        self.task2 = Task.objects.create(
            name="Task 2",
            description="Description 2",
            status=self.status_in_progress,
            author=self.user2,
        )
        self.task2.labels.add(self.label_feature)

        self.client.login(username="testuser", password="StrongPass123")

    def test_filter_by_status(self):
        response = self.client.get(
            reverse("task_list"), {"status": self.status_new.pk}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Task 1")
        self.assertNotContains(response, "Task 2")

    def test_filter_by_assigned_to(self):
        self.task1.assigned_to = self.user2
        self.task1.save()
        response = self.client.get(
            reverse("task_list"), {"assigned_to": self.user2.pk}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Task 1")

    def test_filter_by_labels(self):
        response = self.client.get(
            reverse("task_list"), {"labels": self.label_bug.pk}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Task 1")
        self.assertNotContains(response, "Task 2")

    def test_filter_my_tasks(self):
        response = self.client.get(reverse("task_list"), {"my_tasks": "on"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Task 1")
        self.assertNotContains(response, "Task 2")
