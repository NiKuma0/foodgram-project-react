from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.db import models

User = get_user_model()


class TagModel(models.Model):
    name = models.CharField(_('name'), max_length=200, unique=True)
    color = ColorField(unique=True, format='hex')
    slug = models.SlugField(_('slug'), max_length=200)

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    def __str__(self) -> str:
        return str(self.slug)


class IngredientModel(models.Model):
    name = models.CharField(_('name'), max_length=200, unique=True)
    measurement_unit = models.CharField(_('unit'), max_length=50)

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'ingredients'

    def __str__(self) -> str:
        return self.name


class CountModel(models.Model):
    ingredient = models.ForeignKey(
        IngredientModel, related_name='counts', on_delete=models.CASCADE,
    )
    # recipe = models.ForeignKey(
    #     RecipeModel, models.CASCADE, related_name=_('ingredients')
    # )
    amount = models.IntegerField()


class RecipeModel(models.Model):
    author = models.ForeignKey(
        User, verbose_name=_('author'),
        on_delete=models.CASCADE, related_name='recipes'
    )
    tags = models.ManyToManyField(
        TagModel, verbose_name=_('tags'), related_name='recipes'
    )
    image = models.ImageField(_('image'), upload_to='api/recipes/',)
    name = models.CharField(_('name'), max_length=200)
    text = models.TextField(_('text'))
    cooking_time = models.IntegerField(_('cooking time'))
    ingredients = models.ManyToManyField(
        CountModel, verbose_name=_('ingredients'), related_name='recipe'
    )

    def __str__(self) -> str:
        return _('Recipe') + f' {self.id}, {self.name}'


class FavoriteModel(models.Model):
    user = models.ForeignKey(
        User, verbose_name=_('user'),
        on_delete=models.CASCADE, related_name='favorites'
    )
    recipes = models.ForeignKey(
        RecipeModel, verbose_name=_('recipes'),
        on_delete=models.CASCADE, related_name='likes'
    )


class ShoppingCartModel(models.Model):
    user = models.ForeignKey(
        User, verbose_name=_('user'),
        on_delete=models.CASCADE, related_name='cart'
    )
    recipe = models.ForeignKey(
        RecipeModel, verbose_name=_('recipe'),
        on_delete=models.CASCADE, related_name='shop'
    )
