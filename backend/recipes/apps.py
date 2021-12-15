from django.apps import AppConfig
from django.utils.translation import pgettext_lazy


class RecipesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipes'
    verbose_name = pgettext_lazy('Recipes', 'Рецепты')
