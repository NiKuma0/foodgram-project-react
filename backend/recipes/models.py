from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        _('name'), max_length=200, unique=True, help_text='Назание тэг'
    )
    color = ColorField(unique=True, format='hex', help_text='Цвет тэга')
    slug = models.SlugField(
        _('slug'), max_length=200, help_text='Краткое название тэга'
    )

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self) -> str:
        return str(self.slug)


class Ingredient(models.Model):
    name = models.CharField(
        _('name'), max_length=200, unique=True,
        help_text='Название ингредиента'
    )
    measurement_unit = models.CharField(
        _('unit'), max_length=50, help_text='Единица измерения'
    )

    class Meta:
        verbose_name = _('Ingredient')
        verbose_name_plural = _('Ingredients')

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User, verbose_name=_('author'),
        on_delete=models.CASCADE, related_name='recipes',
        help_text='автор'
    )
    tags = models.ManyToManyField(
        Tag, verbose_name=_('tags'), related_name='recipes',
        help_text='Тэг'
    )
    image = models.ImageField(
        _('image'), upload_to='api/recipes/',
        help_text='Картинка'
    )
    name = models.CharField(
        _('name'), max_length=200,
        help_text='Название рецепта'
    )
    text = models.TextField(
        _('text'), help_text='Описание'
    )
    cooking_time = models.IntegerField(
        _('cooking time'), help_text='Время готовки'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return f'{_("Recipe")} {self.id}, {self.name}'


class Count(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, related_name='counts',
        on_delete=models.CASCADE, help_text='Ингредиент'
    )
    amount = models.PositiveIntegerField(help_text='Количество')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='ingredients', help_text='Рецепт',
        null=True
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return f'{self.ingredient.name} {self.amount}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User, verbose_name=_('user'),
        on_delete=models.CASCADE, related_name='favorites',
        help_text='Пользаватель'
    )
    recipes = models.ForeignKey(
        Recipe, verbose_name=_('recipes'),
        on_delete=models.CASCADE, related_name='likes',
        help_text='Рецепт'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipes'), name='favorite_unique_link'
            ),
        )
        verbose_name = _('Favorite')

    def __str__(self) -> str:
        return f'{self.user.email} {self.recipes.name}'


class ShoppingCart(models.Model):
    user = models.OneToOneField(
        User, verbose_name=_('user'),
        on_delete=models.CASCADE, related_name='cart',
        help_text='Пользователь'
    )
    recipe = models.ManyToManyField(
        Recipe, verbose_name=_('recipe'),
        related_name='shop', help_text='Рецепт'
    )

    class Meta:
        verbose_name = _('Shopping cart')

    def __str__(self) -> str:
        return f'{self.user.email} * {self.recipe}'
