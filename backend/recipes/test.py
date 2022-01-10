from django.contrib.auth import get_user_model

from recipes.models import Recipe
from recipes.serializers import VerboseRecipeSerializer as Serializer

user = get_user_model().objects.first()

class Request:
    user = user

recipe = Recipe.objects.first()
ser = Serializer(
    data={
        'ingredients': [{'id': 1, 'amount': 10}]
    },
    instance=recipe,
    context={'request': Request}
)

