from django.contrib import admin

from recipes.models import Count


class IngredientsInline(admin.TabularInline):
    model = Count
    extra = 1
    verbose_name = 'Ингредиент'
    verbose_name_plural = 'Ингредиенты'
