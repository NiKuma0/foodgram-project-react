from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from recipes.models import Favorite, Recipe
from tools.tests import check_db_test

User = get_user_model()


class FavoriteTestAPI(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create(email='user@mail.com')
        cls.ingredients = Recipe.objects.bulk_create([
            Recipe(
                name=f'test{num}', id=num,
                author=cls.user, cooking_time=1
            )
            for num in range(4)
        ])

    def setUp(self) -> None:
        self.client = APIClient()
        self.client.force_authenticate(FavoriteTestAPI.user)

    @check_db_test(Favorite)
    def test_get(self):
        pk = Recipe.objects.all()[0].id
        url = f'/api/recipes/{pk}/favorite/'
        data = (
            {
                'client': self.client,
                'method': 'post'
            },
            {
                'http': status.HTTP_201_CREATED
            }
        ), (
            {
                'client': self.client,
                'method': 'post'
            },
            {
                'http': status.HTTP_400_BAD_REQUEST
            }
        ), (
            {
                'client': self.client,
                'method': 'delete'
            },
            {
                'http': status.HTTP_204_NO_CONTENT
            }
        ), (
            {
                'client': self.client,
                'method': 'delete'
            },
            {
                'http': status.HTTP_404_NOT_FOUND
            }
        )
        return url, data

    @classmethod
    def tearDownClass(cls) -> None:
        Recipe.objects.all().delete()
        User.objects.all().delete()
