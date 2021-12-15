import tempfile

from django.http.response import HttpResponse
from rest_framework import filters, permissions as perm
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
    TagSerializer, IngredientSerializer, RecipeSerializer, PostRecipeSerializer
)
from tools.views import GetViewSet, FromToViewSet
from .filters import RecipeFilter
from .models import (
    TagModel, RecipeModel, IngredientModel,
    FavoriteModel, ShoppingCartModel
)


class TagViewSet(GetViewSet):
    queryset = TagModel.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(GetViewSet):
    queryset = IngredientModel.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class RecipeViewSet(ModelViewSet):
    queryset = RecipeModel.objects.all()
    serializer_class = RecipeSerializer
    post_serializer_class = PostRecipeSerializer
    permission_classes = (perm.IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT'):
            return self.post_serializer_class
        return self.serializer_class

    def get_object(self):
        return super().get_object()


class FavoriteViewSet(FromToViewSet):
    class Meta:
        from_model = RecipeModel
        to_model = FavoriteModel
        expr = ('recipes', 'user')


class ShoppingCartViewSet(FromToViewSet):
    class Meta:
        from_model = RecipeModel
        to_model = ShoppingCartModel
        expr = ('recipe', 'user')

    def retrieve_data(self, obj: ShoppingCartModel):
        serializer = RecipeSerializer(
            instance=obj.recipe,
            fields=('id', 'name', 'image', 'cooking_time')
        )
        return serializer.data

    def list(self, request):
        file = tempfile.NamedTemporaryFile()
        file.write(self.get_content())
        file.seek(0)
        return HttpResponse(file, content_type='application/txt')

    def get_content(self):
        content = ''
        column = {}
        shop_cart = self.request.user.cart.all()
        for shop_model in shop_cart:
            ingredients = shop_model.recipe.ingredients.all()
            for count_model in ingredients:
                ingr = count_model.ingredient
                column.setdefault(ingr.name, [0, ingr.measurement_unit])
                column[ingr.name][0] += count_model.amount
        for name, val in column.items():
            content += (
                '{} {} {}\n'.format(name, *val)
            ) or 'пусто'
        return bytes(content, 'utf-8')
