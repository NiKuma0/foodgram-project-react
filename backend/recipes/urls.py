from rest_framework.routers import DefaultRouter
from django.urls import path

from recipes.views import (
    TagViewSet, RecipeViewSet,
    IngredientViewSet, FavoriteViewSet,
    ShopingCartViewSet
)

router = DefaultRouter()
router.register('tags', TagViewSet, 'tags')
router.register('recipes', RecipeViewSet, 'recipe')
router.register('recipes', FavoriteViewSet, 'favorite')
router.register('ingredients', IngredientViewSet, 'ingredients')

urlpatterns = [
    path(
        'recipes/download_shopping_cart/',
        ShopingCartViewSet.as_view({'get': 'download_shopping_cart'})
    ),
    path(
        'recipes/<int:pk>/shopping_cart/',
        ShopingCartViewSet.as_view(
            {'post': 'shopping_cart', 'delete': 'destroy'})
    ),
] + router.urls
