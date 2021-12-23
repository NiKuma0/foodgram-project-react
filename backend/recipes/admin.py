from django.contrib import admin

from recipes.models import (
    Tag, Recipe, Ingredient,
    Count, Favorite, ShoppingCart
)


@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color', 'id')
    search_field = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',), }


@admin.register(Recipe)
class AdminRecipe(admin.ModelAdmin):
    list_display = (
        'author', 'name', 'id'
    )
    search_field = ('name', 'text')
    filter_field = ('author', 'cooking_time')


@admin.register(Ingredient)
class AdminIngredient(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit', 'id')
    search_field = ('name',)


@admin.register(Count)
class AdminCount(admin.ModelAdmin):
    list_display = ('ingredient', 'amount', 'id')
    search_field = ('ingredient',)


@admin.register(Favorite)
class AdminFavorite(admin.ModelAdmin):
    list_display = ('user', 'recipes')
    search_field = ('user',)


@admin.register(ShoppingCart)
class AdminShoppingCart(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_field = ('user',)
