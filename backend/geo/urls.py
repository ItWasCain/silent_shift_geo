from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import PointViewSet, RegisterUserView, MessageViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

router = DefaultRouter()
router.register(
    r'points',
    PointViewSet,
    basename='point'
)
router.register(
    r'messages',
    MessageViewSet,
    basename='message'
)

urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),
    path(
        'api/',
        include(router.urls)
    ),
    path(
        'api/auth/register/',
        RegisterUserView.as_view(),
        name='register'
    ),
    path(
        'api/auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'api/auth/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'api/auth/token/verify/',
        TokenVerifyView.as_view(),
        name='token_verify'
    ),
    path(
        'api/auth/',
        include('rest_framework.urls')
    ),
]
