from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    """Основная сущность – Задача."""

    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True)

    # связи – строковые ссылки, чтобы избежать импорт-циклов
    assigned_to = models.ForeignKey(
        User,
        verbose_name=_("Assigned to"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks_assigned",
    )
    status = models.ForeignKey(
        "statuses.Status",
        verbose_name=_("Status"),
        on_delete=models.PROTECT,
        related_name="tasks",
    )
    author = models.ForeignKey(
        User,
        verbose_name=_("Author"),
        on_delete=models.PROTECT,
        related_name="tasks_created",
    )
    labels = models.ManyToManyField(
        "labels.Label",
        verbose_name=_("Labels"),
        blank=True,
        related_name="tasks",
    )

    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    def __str__(self) -> str:
        return self.name
