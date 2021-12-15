from django.http import Http404
from rest_framework import status, permissions as perm
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins, ViewSet, generics


class GetViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 GenericViewSet):
    pass


class FromToViewSet(ViewSet):
    permission_classes = (perm.IsAuthenticated,)
    errors = {
        'already_have': 'You already have this {_from} in your {_to}'
    }

    class Meta:
        from_model = None
        to_model = None
        expr = []

    def retrieve(self, request, pk):
        _o, created = self.get_object(pk, 'get_or_create')
        if not created:
            return Response(
                {'errors': self.get_error('already_have')},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(self.retrieve_data(_o), status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        obj = self.get_object(pk)
        obj.delete()
        return Response(
            self.destroy_data(obj), status=status.HTTP_204_NO_CONTENT
        )

    def get_object(self, pk, method='get', **kwargs):
        from_model = self.Meta.from_model
        to_model = self.Meta.to_model
        expr = self.Meta.expr
        to_obj = generics.get_object_or_404(from_model.objects.all(), pk=pk)
        try:
            obj = getattr(to_model.objects, method)(
                **{expr[0]: to_obj, expr[1]: self.get_from_obj(**kwargs)}
            )
        except to_model.DoesNotExist:
            raise Http404
        return obj

    def get_from_obj(self, **kwargs):
        return self.request.user

    def get_error(self, key):
        msg = self.errors.get(key)
        _from = self.Meta.from_model._meta.verbose_name.lower()
        _to = self.Meta.to_model._meta.verbose_name.lower()
        return msg.format(_from=_from, _to=_to)

    def retrieve_data(self, _o):
        return None

    def destroy_data(self, _o):
        return None
