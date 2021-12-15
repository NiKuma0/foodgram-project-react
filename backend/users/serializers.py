from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from tools.serializers import DynamicFieldsModelSerializer
from recipes.serializers import RecipeSerializer
from .models import SubcribeModel

User = get_user_model()


def sub_to_self(data):
    user = data.get('user')
    to = data.get('pk')
    if user == to:
        raise serializers.ValidationError(
            _('You cannot subscribe to yourself'),
            code='errors'
        )


def unique_subs(data):
    user = data.get('user')
    to = data.get('pk')
    exists = SubcribeModel.objects.filter(
        subscriber=user, subscribed=to
    ).exists()
    if exists:
        raise serializers.ValidationError(
            _('You have already subscribed'),
            # code='errors'
        )


class SubSerializer(serializers.Serializer):
    pk = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=True
    )
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        validators = (sub_to_self, unique_subs)

    def create(self, validated_data):
        user = validated_data.get('user')
        to = validated_data.get('pk')
        return SubcribeModel.objects.create(
            subscriber=user, subscribed=to)


class UserSerializer(DynamicFieldsModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name',
            'password', 'is_subscribed',
            'recipes'
        )
        extra_kwargs = {
            'password': {'write_only': True, 'required': True, },
            'id': {'read_only': True, 'required': False, },
            'email': {'required': True, },
            'username': {'required': True, },
            'first_name': {'required': True, },
            'last_name': {'required': True, }
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user: User = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

    def get_recipes(self, obj):
        request = self.context['request']
        recipe_fields = self.context.get(
            'recipe_fields', {'exclude': ('author',)}
        )
        try:
            value = request.query_params.get('recipes_limit')
            recipes_limit = value if value is None else int(value)
        except ValueError:
            pass
        serializer = RecipeSerializer(
            # instance=obj.recipes.all()[:recipes_limit], many=True,
            instance=obj.recipes.all()[:recipes_limit], many=True,
            read_only=True, context={'request': request},
            **recipe_fields
        )
        return serializer.data

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return SubcribeModel.objects.filter(
            subscriber=user.id, subscribed=obj.id
        ).exists()
