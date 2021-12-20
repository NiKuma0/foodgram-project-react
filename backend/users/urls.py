from rest_framework.routers import DefaultRouter
from django.urls import path, include

from users.views import DynamicUserViewSet, SubscribeViewSet

router = DefaultRouter()
router.register('users', DynamicUserViewSet, basename='user')

urlpatterns = [
    path(
        'users/<pk>/subscribe/', SubscribeViewSet.as_view({
            'delete': 'destroy',
            'get': 'retrieve'
        })
    ),
    path('users/subscriptions/', SubscribeViewSet.as_view({
        'get': 'list'
    })),
    path('', include(router.urls)),
]
