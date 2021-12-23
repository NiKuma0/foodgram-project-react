from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.viewsets import mixins
from rest_framework.response import Response

from users.serializers import SubSerializer, UserSerializer
from tools.views import PkCreateViewSet

User = get_user_model()


class DynamicUserViewSet(UserViewSet):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            exclude=('is_subscribed', 'recipes', 'count_recipes')
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def get_serializer(self, *args, **kwargs):
        kwargs.setdefault('exclude', ('recipes', 'count_recipes'))
        return super().get_serializer(*args, **kwargs)


class SubscribeViewSet(PkCreateViewSet, mixins.ListModelMixin,):
    creation_serializer_class = SubSerializer
    serializer_class = UserSerializer
    lookup_field = 'subscribed'
    lookup_url_kwarg = 'pk'

    def get_serializer_context(self):
        data = super().get_serializer_context()
        data['recipe_fields'] = {'fields': ('id', 'name', 'cooking_time')}
        return data

    def get_queryset(self):
        queryset = self.request.user.subscribed.all()
        if self.request.method == 'GET':
            return [obj.subscribed for obj in queryset]
        return queryset
