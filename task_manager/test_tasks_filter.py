from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task, Status, Label


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
