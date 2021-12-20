from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers as serial
from drf_base64.fields import Base64ImageField

from tools.serializers import DynamicFieldsModelSerializer
from recipes.fields import SerializerRaelatedField, Tag
from recipes.models import TagModel, RecipeModel, IngredientModel, CountModel


class TagSerializer(serial.ModelSerializer):
    class Meta:
        model = TagModel
        fields = '__all__'
        read_only_fields = ('name', 'color', 'slug',)


class IngredientSerializer(serial.ModelSerializer):
    class Meta:
        model = IngredientModel
        fields = '__all__'


class CountSerializer(serial.ModelSerializer):
    id = serial.IntegerField(write_only=True, required=False)
    ingredient = IngredientSerializer(read_only=True)
    amount = serial.IntegerField(required=True)

    class Meta:
        model = CountModel
        fields = ('amount', 'ingredient', 'id')

    def to_internal_value(self, data):
        field = self.fields.pop('id')
        errors = {}
        try:
            pk = field.run_validation(data.pop('id'))
            ingredient = IngredientModel.objects.get(pk=pk)
        except serial.ValidationError as exc:
            errors[field.field_name] = exc.detail
        except IngredientModel.DoesNotExist:
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
    tags = TagSerializer(many=True)
    author = serial.SerializerMethodField()
    image = Base64ImageField()
    ingredients = CountSerializer(
        many=True
    )
    is_favorited = serial.SerializerMethodField()
    is_in_shopping_cart = serial.SerializerMethodField()

    class Meta:
        model = RecipeModel
        fields = (
            'id', 'tags', 'ingredients',
            'image', 'name', 'text',
            'cooking_time', 'author',
            'is_favorited', 'is_in_shopping_cart'
        )

    def get_author(self, obj):
        from users.serializers import UserSerializer
        return UserSerializer(
            instance=obj.author, context=self.context, exclude=('recipes',)
        ).data

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        b = obj.likes.all().filter(user=user.id).exists()
        return b

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        b = obj.shop.all().filter(user=user.id).exists()
        return b


class PostRecipeSerializer(serial.ModelSerializer):
    tags = Tag(TagModel, child=TagSerializer())
    ingredients = SerializerRaelatedField(
        CountSerializer, create=True, many=True
    )
    image = Base64ImageField(required=True)

    class Meta:
        model = RecipeModel
        fields = (
            'author', 'tags', 'ingredients',
            'image', 'name', 'text', 'cooking_time'
        )
        extra_kwargs = {'author': {'read_only': True}}
