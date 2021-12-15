import random as rnd

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from recipes.models import IngredientModel


class IngredientTestAPI(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.ingredients = [
            IngredientModel(
                name=f'ингридиент {num}', id=num,
                measurement_unit=rnd.choice(('кг', 'г', 'шт')),
            ) for num in range(100)
        ]
        IngredientModel.objects.bulk_create(cls.ingredients)

    def setUp(self) -> None:
        self.client = APIClient()

    def test_get_objects(self):
        url = '/api/ingredients/'
        answer = [
            {
                'id': obj.id,
                'name': obj.name,
                'measurement_unit': obj.measurement_unit,
            } for obj in IngredientModel.objects.all()
        ]
        with self.subTest(url=url):
            responce = self.client.get(url)
            self.assertEqual(responce.status_code, status.HTTP_200_OK)
            self.assertEqual(responce.json(), answer)

    def test_get_object(self):
        id = rnd.randint(0, 99)
        url = f'/api/ingredients/{id}/'
        obj = IngredientModel.objects.get(id=id)
        answer = {
            'id': obj.id,
            'name': obj.name,
            'measurement_unit': obj.measurement_unit,
        }
        with self.subTest(url=url):
            responce = self.client.get(url)
            self.assertEqual(responce.status_code, status.HTTP_200_OK)
            self.assertEqual(responce.json(), answer)

    @classmethod
    def tearDownClass(cls):
        IngredientModel.objects.all().delete()
