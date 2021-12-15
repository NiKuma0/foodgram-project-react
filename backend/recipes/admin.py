from django.contrib import admin

from .models import (
    TagModel, RecipeModel, IngredientModel,
    CountModel, FavoriteModel, ShoppingCartModel
)


@admin.register(TagModel)
class AdminTag(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color', 'id')
    search_field = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',), }


@admin.register(RecipeModel)
class AdminRecipe(admin.ModelAdmin):
    list_display = (
        'author', 'name', 'id'
    )
    search_field = ('name', 'text')
    filter_field = ('author', 'cooking_time')


@admin.register(IngredientModel)
class AdminIngredient(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit', 'id')
    search_field = ('name',)


@admin.register(CountModel)
class AdminCount(admin.ModelAdmin):
    list_display = ('ingredient', 'amount', 'id')
    search_field = ('ingredient',)


@admin.register(FavoriteModel)
class AdminFavorite(admin.ModelAdmin):
    list_display = ('user', 'recipes')
    search_field = ('user',)


@admin.register(ShoppingCartModel)
class AdminShoppingCart(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_field = ('user',)
