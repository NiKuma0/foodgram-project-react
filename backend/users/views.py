from django.contrib.auth import get_user_model
from rest_framework.viewsets import GenericViewSet
from rest_framework import status, permissions as perm
from rest_framework.response import Response
from rest_framework.request import Request

from users.serializers import SubSerializer, VerboseUserSerializer

User = get_user_model()


class SubscribeViewSet(GenericViewSet):
    permission_classes = (perm.IsAuthenticated,)
    serializer_class = VerboseUserSerializer
    lookup_field = 'subscribed'
    lookup_url_kwarg = 'pk'

    def subscribe(self, request, pk):
        serializer = SubSerializer(
            data={self.lookup_field: pk},
            context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        serializer = self.get_serializer(
            instance=instance.subscribed
        )
        return Response(
            serializer.data, status=status.HTTP_201_CREATED
        )

    def destroy(self, request, *args, **kwargs):
        self.get_object().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def subscriptions(self, request: Request):
        queryset = [sub.subscribed for sub in request.user.subscribed.all()]
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = self.request.user.subscribed.all()
        return queryset
