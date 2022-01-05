from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, validators as valid

from users.validators import not_equal
from users.models import Subcribe

User = get_user_model()


class SubSerializer(serializers.ModelSerializer):
    subscriber = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Subcribe
        fields = '__all__'
        validators = (
            not_equal(
                'subscriber', 'subscribed',
                _('You cannot subscribe to yourself')
            ),
            valid.UniqueTogetherValidator(
                Subcribe.objects.all(),
                ('subscriber', 'subscribed'),
                _('You have already subscribed')
            )
        )

    @property
    def data(self):
        return UserSerializer(
            instance=self.validated_data['subscribed'],
            context=self.context,
            exclude=('is_subscribed',)
        ).data


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name',
            'is_subscribed', 'password'
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
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

    def get_is_subscribed(self, instance_user):
        request = self.context.get('request')
        user = getattr(request, 'user', AnonymousUser)
        if not user.is_authenticated:
            return False
        return Subcribe.objects.filter(
            subscriber=user.id, subscribed=instance_user.id
        ).exists()


class VerboseUserSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipe_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name',
            'recipes', 'recipe_count',
            'is_subscribed',
        )

    def get_recipes(self, user):
        from recipes.serializers import RecipeSerializer
        return RecipeSerializer(
            instance=user.recipes.all(), many=True,
            context=self.context
        ).data

    def get_recipe_count(self, user):
        return user.recipes.count()
