import tempfile

from django.http.response import HttpResponse
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters, permissions as perm
from rest_framework.decorators import action
from rest_framework.viewsets import mixins, ModelViewSet, GenericViewSet
from rest_framework.response import Response

from recipes.serializers import (
    TagSerializer, IngredientSerializer, RecipeSerializer,
    FavoriteSerializer, VerboseRecipeSerializer
)
from recipes.filters import RecipeFilter
from recipes.models import (
    Tag, Recipe, Ingredient, ShoppingCart
)


class FavoriteViewSet(GenericViewSet):
    permission_classes = (perm.IsAuthenticated,)
    serializer_class = RecipeSerializer
    lookup_field = 'recipes'
    lookup_url_kwarg = 'pk'

    @action(('POST',), detail=True)
    def favorite(self, request, pk):
        serializer = FavoriteSerializer(
            data={self.lookup_field: pk},
            context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        serializer = self.get_serializer(instance=instance.recipes)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def destroy(self, request, pk):
        self.get_object().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        return self.request.user.favorites.all()


class ShopingCartViewSet(GenericViewSet):
    permission_classes = (perm.IsAuthenticated,)
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    lookup_url_kwarg = 'pk'

    def shopping_cart(self, request, pk):
        recipe = self.get_object()
        cart = self.get_cart()
        cart.recipe.add(recipe)
        serializer = self.get_serializer(instance=recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        recipe = self.get_object()
        cart = self.get_cart()
        cart.recipe.remove(recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def download_shopping_cart(self, request, *args, **kwargs):
        file = tempfile.NamedTemporaryFile()
        file.write(self.get_content())
        file.seek(0)
        return HttpResponse(file, content_type='application/txt')

    def get_content(self):
        cart = self.get_cart()
        ingredients = cart.recipe.values_list(
            'ingredients__ingredient__name',
            'ingredients__ingredient__measurement_unit'
        ).annotate(Sum('ingredients__amount'))
        content = ''
        for ingredient in ingredients:
            content += f'{ingredient[0]} {ingredient[2]} {ingredient[1]};\n'
        return bytes(content, 'utf-8')

    def get_cart(self) -> ShoppingCart:
        o, _ = ShoppingCart.objects.get_or_create(user=self.request.user)
        return o


class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (perm.IsAuthenticatedOrReadOnly,)
    serializer_class = VerboseRecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
