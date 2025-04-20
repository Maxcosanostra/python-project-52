from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UserCrudTests(TestCase):
    def test_registration_redirects_to_login(self):
        response = self.client.post(
            reverse("user_create"),
            {
                "username": "testuser",
                "password1": "StrongPassword123",
                "password2": "StrongPassword123",
            },
        )
        self.assertRedirects(response, reverse("login"))

    def test_login_redirects_to_home(self):
        User.objects.create_user(
            username="testuser", password="StrongPassword123"
        )
        response = self.client.post(
            reverse("login"),
            {"username": "testuser", "password": "StrongPassword123"},
        )
        self.assertRedirects(response, reverse("index"))

    def test_update_redirects_to_user_list(self):
        user = User.objects.create_user(
            username="testuser", password="StrongPassword123"
        )
        self.client.login(username="testuser", password="StrongPassword123")
        response = self.client.post(
            reverse("user_update", args=[user.pk]),
            {
                "username": "testuser_updated",
            },
        )
        self.assertRedirects(response, reverse("user_list"))

    def test_delete_redirects_to_user_list(self):
        user = User.objects.create_user(
            username="testuser", password="StrongPassword123"
        )
        self.client.login(username="testuser", password="StrongPassword123")
        response = self.client.post(reverse("user_delete", args=[user.pk]))
        self.assertRedirects(response, reverse("user_list"))
