from rest_framework import status, permissions as perm
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins


class GetViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 GenericViewSet):
    pass


class PkCreateViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    permission_classes = (perm.IsAuthenticated,)
    serializer_class = ...
    creation_serializer_class = None
    link_field = None
    lookup_field = ...
    lookup_url_kwarg = ...

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        data[self.lookup_field] = self.kwargs.get(self.lookup_url_kwarg)
        serializer, its_creation_serializer = self.get_creation_serializer(
            data=data
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        if its_creation_serializer:
            serializer = self.get_serializer(
                instance=serializer.validated_data.get(
                    self.link_field or self.lookup_field
                )
            )
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def get_creation_serializer(self, *args, **kwargs):
        serializer_class = self.creation_serializer_class
        if serializer_class is None:
            return super().get_serializer(*args, **kwargs), False
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs), True

