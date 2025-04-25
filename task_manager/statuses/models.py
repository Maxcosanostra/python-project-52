from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    name = models.CharField(_("Name"), max_length=100, unique=True)
    created_at = models.DateTimeField(
        _("Date Created"), auto_now_add=True, null=True, blank=True
    )

    class Meta:
        verbose_name = _("Статус")
        verbose_name_plural = _("Статусы")
        ordering = ("pk",)

    def __str__(self) -> str:  # pragma: no cover
        return self.name
