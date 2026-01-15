from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
# from django.contrib.gis.geos import Point

from points.models import Point, User
from chat.models import Message
from .serializers import (
    PointCreateSerializer,
    PointSerializer,
    PointSearchSerializer,
    MessageCreateSerializer,
    MessageSerializer,
    MessageSearchSerializer
)
from .services import GeoSearchService


class BaseViewSetMixin:

    authentication_classes = [JWTAuthentication]

    _permission_map = {
        'create': [IsAuthenticated],
        'search': [IsAuthenticated],
        'list': [IsAuthenticated],
        'retrieve': [IsAuthenticated],
        'destroy': [IsAuthenticated],
        'update': [IsAuthenticated],
        'partial_update': [IsAuthenticated],
    }

    def get_serializer_class(self):
        """Возвращает сериализатор в зависимости от действия."""
        serializer_map = getattr(self, '_serializer_map', {})
        return serializer_map.get(self.action, self.serializer_class)

    def get_permissions(self):
        """Возвращает permissions в зависимости от действия."""
        # Используем permissions из дочернего класса или базовые
        permission_map = getattr(self, '_permission_map', self._permission_map)
        permissions = permission_map.get(self.action, [IsAuthenticated])
        return [permission() for permission in permissions]

    def perform_create(self, serializer):
        """Автоматически назначает автора при создании."""
        serializer.save(author=self.request.user)

    def check_object_permissions(self, request, obj):
        """Проверяет права на удаление/редактирование."""
        if request.method in ['DELETE', 'PUT', 'PATCH']:
            is_author = obj.author == request.user
            is_admin = request.user.is_staff
            if not (is_author or is_admin):
                self.permission_denied(
                    request,
                    message='Только автор или администратор имеют доступ.'
                )
        super().check_object_permissions(request, obj)


class RegisterUserView(generics.CreateAPIView):
    """Создание нового пользователя."""

    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')

        if not username or not password:
            return Response(
                {'error': 'Укажите username и password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            return Response({
                'message': 'Пользователь создан',
                'username': user.username,
                'id': user.id
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class PointViewSet(BaseViewSetMixin, viewsets.ModelViewSet):
    """ViewSet для работы с точками."""

    queryset = Point.objects.all()
    serializer_class = PointSerializer

    _serializer_map = {
        'create': PointCreateSerializer,
        'search': PointSearchSerializer,
    }

    @action(detail=False, methods=['post'])
    def search(self, request):
        """
        Поиск точек в указанном радиусе.

        POST /api/points/search/
        {
            "latitude": 55.7558,
            "longitude": 37.6178,
            "radius_km": 10.0
        }
        """
        serializer = PointSearchSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validated_data = serializer.validated_data

            # Используем универсальный сервис для поиска
            search_service = GeoSearchService()
            queryset = self.get_queryset()

            # Поиск точек напрямую (у них есть поле location)
            results = search_service.search_direct(
                queryset=queryset,
                location_field='location',
                latitude=validated_data['latitude'],
                longitude=validated_data['longitude'],
                radius_km=validated_data['radius_km']
            )

            result_serializer = PointSerializer(results, many=True)

            return Response({
                'count': results.count(),
                'results': result_serializer.data
            })

        except Exception:
            return Response(
                {'error': 'Произошла ошибка при поиске точек'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def create(self, request, *args, **kwargs):
        """Создание новой точки с кастомным ответом."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response_serializer = PointSerializer(serializer.instance)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )


class MessageViewSet(BaseViewSetMixin, viewsets.ModelViewSet):
    """ViewSet для работы с сообщениями."""

    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    # Переопределяем только сериализаторы, permissions наследуются
    _serializer_map = {
        'create': MessageCreateSerializer,
        'search': MessageSearchSerializer,
    }

    @action(detail=False, methods=['post'], url_path='points/messages')
    def create_message_for_point(self, request):
        """
        Создание сообщения к заданной точке.

        POST /api/points/messages/
        {
            "point": 1,
            "content": "Текст сообщения"
        }
        """
        serializer = MessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        response_serializer = MessageSerializer(serializer.instance)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['post'])
    def search(self, request):
        """
        Поиск сообщений в заданном радиусе.

        POST /api/messages/search/
        {
            "latitude": 55.7558,
            "longitude": 37.6178,
            "radius_km": 10.0
        }
        """
        serializer = MessageSearchSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validated_data = serializer.validated_data

            # Используем универсальный сервис для поиска
            search_service = GeoSearchService()
            queryset = self.get_queryset()

            # Поиск сообщений через связанные точки
            messages = search_service.search_through_points(
                objects_queryset=queryset,
                point_model=Point,
                point_field='point',
                latitude=validated_data['latitude'],
                longitude=validated_data['longitude'],
                radius_km=validated_data['radius_km']
            )

            result_serializer = MessageSerializer(messages, many=True)

            return Response({
                'count': messages.count(),
                'results': result_serializer.data
            })

        except Exception:
            return Response(
                {'error': 'Произошла ошибка при поиске сообщений'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
