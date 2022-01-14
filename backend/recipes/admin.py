from django.contrib import admin

from recipes.forms import IngredientsInline
from recipes.models import (
    Tag, Recipe, Ingredient,
    Count, Favorite, ShoppingCart
)


@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color', 'id')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',), }


@admin.register(Recipe)
class AdminRecipe(admin.ModelAdmin):
    list_display = (
        'author', 'name', 'id',
    )
    inlines = (IngredientsInline,)
    search_fields = ('name', 'text', 'author__email', 'author__username')
    filter_field = ('author', 'cooking_time')


@admin.register(Ingredient)
class AdminIngredient(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit', 'id')
    search_fields = (
        'name', 'recipe__name',
        'recipe__author__email', 'recipe__author__username'
    )


@admin.register(Count)
class AdminCount(admin.ModelAdmin):
    list_display = ('ingredient', 'amount', 'id')
    search_fields = ('ingredient',)


@admin.register(Favorite)
class AdminFavorite(admin.ModelAdmin):
    list_display = ('user', 'recipes')
    search_fields = ('user__email', 'user__username', 'recipes__name')


@admin.register(ShoppingCart)
class AdminShoppingCart(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__email', 'user__username')
