from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
from django.conf import settings

User = get_user_model()


class Point(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")

    # Точка с координатами (x=долгота, y=широта)
    location = models.PointField(
        verbose_name="Координаты",
        geography=True,
        srid=4326,
        null=True,
        blank=True
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name="points",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Точка"
        verbose_name_plural = "Точки"
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name

    @property
    def latitude(self):
        """Возвращает широту"""
        if self.location:
            return self.location.y
        return None

    @property
    def longitude(self):
        """Возвращает долготу"""
        if self.location:
            return self.location.x
        return None

    @property
    def coordinates(self):
        """Возвращает координаты в виде кортежа (lat, lon)"""
        if self.location:
            return (self.location.y, self.location.x)
        return (None, None)
