from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .statuses.models import Status


class StatusCrudTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="StrongPassword123"
        )
        self.client.login(username="testuser", password="StrongPassword123")
        self.status = Status.objects.create(name="New")

    def test_status_list_view(self):
        response = self.client.get(reverse("status_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "New")

    def test_status_create_view(self):
        response = self.client.post(
            reverse("status_create"), {"name": "In Progress"}
        )
        self.assertRedirects(response, reverse("status_list"))
        self.assertTrue(Status.objects.filter(name="In Progress").exists())

    def test_status_update_view(self):
        response = self.client.post(
            reverse("status_update", args=[self.status.pk]),
            {"name": "Completed"},
        )
        self.assertRedirects(response, reverse("status_list"))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, "Completed")

    def test_status_delete_view(self):
        response = self.client.post(
            reverse("status_delete", args=[self.status.pk])
        )
        self.assertRedirects(response, reverse("status_list"))
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())
