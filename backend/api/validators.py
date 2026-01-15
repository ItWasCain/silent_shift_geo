from rest_framework import serializers


def validate_coordinates(latitude, longitude):
    """Проверяет корректность географических координат."""
    if not (-90 <= latitude <= 90):
        raise serializers.ValidationError(
            "Широта должна быть в диапазоне от -90 до 90."
        )

    if not (-180 <= longitude <= 180):
        raise serializers.ValidationError(
            "Долгота должна быть в диапазоне от -180 до 180."
        )

    return latitude, longitude


def validate_positive_number(value, field_name):
    """Проверяет, что значение положительное."""
    if value <= 0:
        raise serializers.ValidationError(
            f"{field_name} должен быть положительным числом."
        )
    return value
