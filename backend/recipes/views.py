import tempfile

from django.http.response import HttpResponse
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions as perm
from rest_framework.viewsets import ModelViewSet

from recipes.serializers import (
    TagSerializer, IngredientSerializer, RecipeSerializer,
    FavoriteSerializer, ShopingCartSerializer
)
from tools.views import GetViewSet, PkCreateViewSet
from recipes.filters import RecipeFilter
from recipes.models import (
    Tag, Recipe, Ingredient, ShoppingCart
)


class FavoriteViewSet(PkCreateViewSet):
    serializer_class = FavoriteSerializer
    lookup_field = 'recipes'
    lookup_url_kwarg = 'pk'

    def get_queryset(self):
        return self.request.user.favorites.all()


class ShopingCartViewSet(PkCreateViewSet):
    serializer_class = ShopingCartSerializer
    lookup_field = 'recipe'
    lookup_url_kwarg = 'pk'

    def list(self, *args, **kwargs):
        file = tempfile.NamedTemporaryFile()
        file.write(self.get_content())
        file.seek(0)
        return HttpResponse(file, content_type='application/txt')

    def get_content(self):
        FORMAT = '{0.name} {0.amount} {0.measurement_unit};'
        user = self.request.user
        recipes = [
            shop.recipe for shop in ShoppingCart.objects.filter(user=user)
        ]
        ingredients = Ingredient.objects.filter(
            counts__recipe__in=recipes
        )
        cart = ingredients.annotate(amount=Sum('counts__amount'))
        content = '\n'.join(map(FORMAT.format, cart))
        return bytes(content, 'utf-8')

    def get_queryset(self):
        return self.request.user.cart.all()


class TagViewSet(GetViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(GetViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (perm.IsAuthenticatedOrReadOnly,)
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_object(self):
        return super().get_object()

    def get_serializer_context(self):
        data = super().get_serializer_context()
        data['author_exclude'] = ('recipes', 'count_recipes')
        return data
