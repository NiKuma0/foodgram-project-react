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
    FavoriteSerializer, ShopingCartSerializer, VerboseRecipeSerializer
)
from recipes.filters import RecipeFilter
from recipes.models import (
    Tag, Recipe, Ingredient
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
    lookup_field = 'recipe'
    lookup_url_kwarg = 'pk'

    def shopping_cart(self, request, pk):
        serializer = ShopingCartSerializer(
            data={self.lookup_field: pk},
            context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        serializer = self.get_serializer(instance=instance.recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        self.get_object().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def download_shopping_cart(self, *args, **kwargs):
        file = tempfile.NamedTemporaryFile()
        file.write(self.get_content())
        file.seek(0)
        return HttpResponse(file, content_type='application/txt')

    def get_content(self):
        user = self.request.user
        recipes = user.cart.all().values('recipe')
        cart = Ingredient.objects.filter(
            counts__recipe__in=recipes
        ).annotate(amount=Sum('counts__amount'))
        content = ''
        for ingr in cart:
            content += f'{ingr.name} {ingr.amount} {ingr.measurement_unit};\n'
        return bytes(content, 'utf-8')

    def get_queryset(self):
        return self.request.user.cart.all()


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

    def get_object(self):
        return super().get_object()
