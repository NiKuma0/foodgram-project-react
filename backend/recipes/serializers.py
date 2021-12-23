from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers as serial
from drf_base64.fields import Base64ImageField

from tools.serializers import DynamicFieldsModelSerializer
from tools.validators import unique_object
from recipes.fields import SerializerRaelatedField, TagField
from recipes.models import (
    Recipe, Count, Ingredient,
    Favorite, ShoppingCart, Tag
)


class FavoriteSerializer(serial.ModelSerializer):
    user = serial.HiddenField(
        default=serial.CurrentUserDefault()
    )

    class Meta:
        model = Favorite
        fields = '__all__'
        validators = (
            unique_object(
                Favorite.objects.all(),
                'user', 'recipes',
                _('You already have this recipe in your favorites')
            ),
        )

    @property
    def data(self):
        return RecipeSerializer(
            instance=self.validated_data['recipes'],
            fields=('id', 'name', 'image', 'cooking_time'),
            context=self.context
        ).data


class ShopingCartSerializer(serial.ModelSerializer):
    user = serial.HiddenField(
        default=serial.CurrentUserDefault()
    )

    class Meta:
        model = ShoppingCart
        fields = '__all__'
        validators = (
            unique_object(
                ShoppingCart.objects.all(),
                'user', 'recipe',
                _('You already have this recipe in your shop cart')
            ),
        )

    @property
    def data(self):
        return RecipeSerializer(
            instance=self.validated_data['recipe'],
            fields=('id', 'name', 'image', 'cooking_time'),
            context=self.context
        ).data


class TagSerializer(serial.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('name', 'color', 'slug',)


class IngredientSerializer(serial.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class CountSerializer(serial.ModelSerializer):
    id = serial.IntegerField(write_only=True, required=False)
    ingredient = IngredientSerializer(read_only=True)
    amount = serial.IntegerField(required=True)

    class Meta:
        model = Count
        fields = ('amount', 'ingredient', 'id')

    def to_internal_value(self, data):
        field = self.fields.pop('id')
        errors = {}
        try:
            pk = field.run_validation(data.pop('id'))
            ingredient = Ingredient.objects.get(pk=pk)
        except serial.ValidationError as exc:
            errors[field.field_name] = exc.detail
        except Ingredient.DoesNotExist:
            raise serial.ValidationError(
                f'ingredient {pk}',
                _('Not found')
            )
        if errors:
            raise serial.ValidationError(errors)
        ret = super().to_internal_value(data)
        return {**ret, 'ingredient': ingredient}

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ingredient = ret.pop('ingredient')
        return {**ret, **ingredient}


class RecipeSerializer(DynamicFieldsModelSerializer):
    tags = TagField(Tag, child=TagSerializer())
    ingredients = SerializerRaelatedField(
        CountSerializer, create=True, many=True
    )
    image = Base64ImageField(required=True)
    author = serial.SerializerMethodField()
    is_favorited = serial.SerializerMethodField()
    is_in_shopping_cart = serial.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'ingredients',
            'image', 'name', 'text',
            'cooking_time', 'author',
            'is_favorited', 'is_in_shopping_cart'
        )
        extra_kwargs = {'author': {'read_only': True}}

    def get_author(self, obj):
        from users.serializers import UserSerializer
        return UserSerializer(
            instance=obj.author, context=self.context,
            exclude=self.context.get('author_exclude', ('recipes',)),
            fields=self.context.get('author_fields', None)
        ).data

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        b = obj.likes.all().filter(user=user.id).exists()
        return b

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        b = obj.shop.all().filter(user=user.id).exists()
        return b
