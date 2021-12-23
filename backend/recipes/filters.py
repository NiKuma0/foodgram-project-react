from django_filters.rest_framework import FilterSet
import django_filters as filters

from recipes.models import Recipe, Tag


class RecipeFilter(FilterSet):
    is_favorited = filters.BooleanFilter(
        method='get_favorite', label='is favorited'
    )
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_shop'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags')

    def get_favorite(self, queryset, name, value):
        if not value:
            return queryset
        user = self.request.user
        return queryset.filter(likes__user=user.id)

    def get_shop(self, queryset, name, value):
        if not value:
            return queryset
        user = self.request.user
        return queryset.filter(shop__user=user.id)
