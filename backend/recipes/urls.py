from rest_framework.routers import DefaultRouter
from django.urls import path, include

from recipes.views import (
    TagViewSet, RecipeViewSet,
    IngredientViewSet, FavoriteViewSet,
    ShoppingCartViewSet
)

tags_router = DefaultRouter()
tags_router.register('tags', TagViewSet, 'tags')
recipes_router = DefaultRouter()
recipes_router.register('recipes', RecipeViewSet, 'recipes')
ingredient_router = DefaultRouter()
ingredient_router.register('ingredients', IngredientViewSet, 'ingredients')

urlpatterns = [
    path('', include(tags_router.urls)),
    path(
        'recipes/<int:pk>/favorite/',
        FavoriteViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})
    ),
    path(
        'recipes/<int:pk>/shopping_cart/',
        ShoppingCartViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})
    ),
    path(
        'recipes/download_shopping_cart/',
        ShoppingCartViewSet.as_view({'get': 'list'})
    ),
    path('', include(recipes_router.urls)),
    path('', include(ingredient_router.urls))
]
