from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    name = models.CharField(
        _("Name"),
        max_length=100,
        unique=True
    )
    created_at = models.DateTimeField(
        _("Date Created"),
        auto_now_add=True,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(
        _("Name"),
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(
        _("Name"),
        max_length=255
    )
    description = models.TextField(
        _("Description"),
        blank=True
    )
    assigned_to = models.ForeignKey(
        User,
        verbose_name=_("Assigned to"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks_assigned"
    )
    status = models.ForeignKey(
        Status,
        verbose_name=_("Status"),
        on_delete=models.PROTECT,
        related_name="tasks"
    )
    author = models.ForeignKey(
        User,
        verbose_name=_("Author"),
        on_delete=models.PROTECT,
        related_name="tasks_created"
    )
    labels = models.ManyToManyField(
        Label,
        verbose_name=_("Labels"),
        blank=True,
        related_name="tasks"
    )
    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True
    )

    def __str__(self):
        return self.name
