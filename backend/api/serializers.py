from rest_framework import serializers
from django.contrib.gis.geos import Point as GeoPoint
from points.models import Point
from chat.models import Message
from .validators import validate_coordinates


class PointCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания точки."""

    latitude = serializers.FloatField(
        write_only=True,
        required=True,
        min_value=-90.0,
        max_value=90.0
    )

    longitude = serializers.FloatField(
        write_only=True,
        required=True,
        min_value=-180.0,
        max_value=180.0
    )

    class Meta:
        model = Point
        fields = ['name', 'latitude', 'longitude']

    def validate(self, data):
        """Создает объект Point из координат."""
        lat = data.pop('latitude')
        lon = data.pop('longitude')

        validate_coordinates(lat, lon)
        data['location'] = GeoPoint(lon, lat, srid=4326)

        return data

    def create(self, validated_data):
        """Создает точку с автором из запроса."""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PointSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения точки."""

    latitude = serializers.FloatField(
        source='location.y',
        read_only=True
    )
    longitude = serializers.FloatField(
        source='location.x',
        read_only=True
    )
    author_username = serializers.CharField(
        source='author.username',
        read_only=True
    )
    distance_km = serializers.FloatField(read_only=True)

    class Meta:
        model = Point
        fields = [
            'id',
            'name',
            'latitude',
            'longitude',
            'distance_km',
            'author',
            'author_username',
            'created_at'
        ]
        read_only_fields = ['id', 'author', 'created_at']


class PointSearchSerializer(serializers.Serializer):
    """Сериализатор для поиска точек."""

    latitude = serializers.FloatField(
        required=True,
        min_value=-90.0,
        max_value=90.0
    )
    longitude = serializers.FloatField(
        required=True,
        min_value=-180.0,
        max_value=180.0
    )
    radius_km = serializers.FloatField(
        required=False,
        default=10.0,
        min_value=0.1,
        max_value=1000.0
    )


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['point', 'content']
        read_only_fields = ['author']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'content', 'author', 'point', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']


class MessageSearchSerializer(serializers.Serializer):
    latitude = serializers.FloatField(required=True)
    longitude = serializers.FloatField(required=True)
    radius_km = serializers.FloatField(required=True, min_value=0.1)
