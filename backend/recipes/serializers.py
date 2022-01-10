from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, validators as valid
from drf_base64.fields import Base64ImageField

from recipes.fields import TagField, SerializerField
from recipes.models import (
    Recipe, Count, Ingredient,
    Favorite, ShoppingCart, Tag
)


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Favorite
        fields = '__all__'
        validators = (
            valid.UniqueTogetherValidator(
                Favorite.objects.all(),
                ('user', 'recipes'),
                _('You already have this recipe in your favorites')
            ),
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('name', 'color', 'slug',)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class CountSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    name = serializers.CharField(read_only=True)
    measurement_unit = serializers.CharField(read_only=True)
    amount = serializers.IntegerField(required=True)

    def create(self, validated_data):
        ingredient = validated_data.pop('id')
        return Count.objects.create(ingredient=ingredient, **validated_data)


class VerboseRecipeSerializer(serializers.ModelSerializer):
    tags = TagField(
        queryset=Tag.objects.all(), child=TagSerializer(), many=True
    )
    author = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField(required=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    ingredients = SerializerField(
        CountSerializer, many=True, required=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time'
        )

    def get_author(self, recipe):
        from users.serializers import UserSerializer
        return UserSerializer(
            instance=recipe.author,
            context=self.context,
            many=False
        ).data

    def get_is_favorited(self, recipe):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if user is None or not user.is_authenticated:
            return False
        return Favorite.objects.filter(recipes=recipe, user=user).exists()

    def get_is_in_shopping_cart(self, recipe):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        return ShoppingCart.objects.filter(
            recipe=recipe, user=user.id
        ).exists()

    def get_ingredients(self, recipe):
        ser = CountSerializer(instance=recipe.ingredients.all(), many=True)
        return ser.data


class ListRecipeSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        limit = self.context['request'].query_params.get('recipes_limit')
        try:
            limit = None if limit is None else int(limit)
        except ValueError:
            raise serializers.ValidationError(
                {'recipes_limit': _('A valid integer is required.')},
            )
        data = data[:limit]
        return super().to_representation(data)


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        list_serializer_class = ListRecipeSerializer
        fields = ('id', 'name', 'image', 'cooking_time')
