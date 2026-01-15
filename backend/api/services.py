from django.contrib.gis.geos import Point as GeoPoint
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.db.models import QuerySet


class GeoSearchService:
    """Универсальный сервис для поиска по геолокации."""

    @staticmethod
    def create_search_point(latitude: float, longitude: float) -> GeoPoint:
        """Создает точку для поиска."""
        return GeoPoint(longitude, latitude, srid=4326)

    @staticmethod
    def km_to_meters(radius_km: float) -> float:
        """Конвертирует километры в метры."""
        return radius_km * 1000

    @staticmethod
    def search_direct(
        queryset: QuerySet,
        location_field: str,  # Поле с координатами
        latitude: float,
        longitude: float,
        radius_km: float
    ) -> QuerySet:
        """
        Поиск объектов с геополем в радиусе.
        """

        center = GeoSearchService.create_search_point(latitude, longitude)
        radius_meters = GeoSearchService.km_to_meters(radius_km)

        return queryset.filter(
            **{f'{location_field}__distance_lte': (center, D(m=radius_meters))}
        ).annotate(
            distance_km=Distance(location_field, center) / 1000
        ).order_by('distance_km')

    @staticmethod
    def search_through_points(
        objects_queryset: QuerySet,
        point_model,
        point_field: str,
        latitude: float,
        longitude: float,
        radius_km: float
    ) -> QuerySet:
        """
        Поиск объектов через связанные точки.
        """

        center = GeoSearchService.create_search_point(latitude, longitude)
        radius_meters = GeoSearchService.km_to_meters(radius_km)

        points_in_radius = point_model.objects.filter(
            location__distance_lte=(center, D(m=radius_meters))
        )

        point_ids = points_in_radius.values_list('id', flat=True)

        # Фильтруем объекты по связи с точками
        return objects_queryset.filter(**{f'{point_field}__in': point_ids})
