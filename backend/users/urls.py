from rest_framework.routers import DefaultRouter
from django.urls import path
from djoser.views import UserViewSet

from users.views import SubscribeViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path(
        'users/subscriptions/',
        SubscribeViewSet.as_view({'get': 'subscriptions'})
    ),
    path(
        'users/<int:pk>/subscribe/',
        SubscribeViewSet.as_view({'post': 'subscribe', 'delete': 'destroy'})
    )
] + router.urls
