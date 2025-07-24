from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import NotificationViewSet, UserViewSet

v1_router = DefaultRouter()
v1_router.register('notifications', NotificationViewSet)
v1_router.register('users', UserViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/token/', views.obtain_auth_token),
    path('', include(v1_router.urls)),
]
