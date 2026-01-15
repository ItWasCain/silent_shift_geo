from django.db import models
from points.models import Point, User


class Message(models.Model):
    """Модель сообщения, привязанного к точке на карте."""

    point = models.ForeignKey(
        Point,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Точка"
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Автор",
        null=True,
        blank=True
    )

    content = models.TextField(
        verbose_name="Текст сообщения"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ['-created_at']

    def __str__(self):
        return f"Сообщение к точке {self.point.name}"
