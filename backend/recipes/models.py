from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(_('name'), max_length=200, unique=True)
    color = ColorField(unique=True, format='hex')
    slug = models.SlugField(_('slug'), max_length=200)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self) -> str:
        return str(self.slug)


class Ingredient(models.Model):
    name = models.CharField(_('name'), max_length=200, unique=True)
    measurement_unit = models.CharField(_('unit'), max_length=50)

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'ingredients'

    def __str__(self) -> str:
        return self.name


class Count(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, related_name='counts', on_delete=models.CASCADE,
    )
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.ingredient.name} {self.amount}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User, verbose_name=_('author'),
        on_delete=models.CASCADE, related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tag, verbose_name=_('tags'), related_name='recipes'
    )
    image = models.ImageField(_('image'), upload_to='api/recipes/',)
    name = models.CharField(_('name'), max_length=200)
    text = models.TextField(_('text'))
    cooking_time = models.IntegerField(_('cooking time'))
    ingredients = models.ManyToManyField(
        Count, verbose_name=_('ingredients'), related_name='recipe'
    )

    def __str__(self) -> str:
        return f'{_("Recipe")} {self.id}, {self.name}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User, verbose_name=_('user'),
        on_delete=models.CASCADE, related_name='favorites'
    )
    recipes = models.ForeignKey(
        Recipe, verbose_name=_('recipes'),
        on_delete=models.CASCADE, related_name='likes'
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
    user = models.ForeignKey(
        User, verbose_name=_('user'),
        on_delete=models.CASCADE, related_name='cart'
    )
    recipe = models.ForeignKey(
        Recipe, verbose_name=_('recipe'),
        on_delete=models.CASCADE, related_name='shop'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'), name='shop_unique_link'
            ),
        )
        verbose_name = _('Shopping cart')

    def __str__(self) -> str:
        return f'{self.user.email} * {self.recipe.name}'
