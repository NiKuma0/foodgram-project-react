from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.response import Response
from djoser.views import UserViewSet

from .models import SubcribeModel
from .serializers import SubSerializer, UserSerializer
from tools.views import FromToViewSet

User = get_user_model()


class DynamicUserViewSet(UserViewSet):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, exclude=('is_subscribed', 'recipes')
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def get_serializer(self, *args, **kwargs):
        kwargs.setdefault('exclude', ('recipes',))
        return super().get_serializer(*args, **kwargs)


class SubscribeViewSet(FromToViewSet,
                       viewsets.mixins.ListModelMixin,
                       viewsets.GenericViewSet):

    serializer_class = UserSerializer

    class Meta:
        from_model = User
        to_model = SubcribeModel
        expr = ('subscribed', 'subscriber')

    def retrieve(self, request, pk):
        ser = SubSerializer(context={'request': request}, data={'pk': pk})
        ser.is_valid(raise_exception=True)
        ser.save()
        sub = UserSerializer(
            instance=ser.validated_data['pk'],
            context={'request': request},
            exclude=('is_subscribed',)
        )
        return Response(sub.data, status=status.HTTP_201_CREATED)

    def get_serializer_context(self):
        data = super().get_serializer_context()
        data['recipe_fields'] = {'fields': ('id', 'name', 'cooking_time')}
        return data

    def get_queryset(self):
        return [
            obj.subscribed for obj in self.request.user.subscribed.all()
        ]
