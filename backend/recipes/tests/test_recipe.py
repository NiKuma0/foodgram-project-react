import random as rnd
import tempfile
# import base64
from io import BytesIO
from PIL import Image
from shutil import rmtree
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from recipes.models import RecipeModel, TagModel, IngredientModel, CountModel
from tools.tests import base_test, check_db_test

MEDIA = tempfile.mktemp()
User = get_user_model()


def data_maping(objects):
    return [{
        'id': obj.id,
        'tags': [{
            'id': tag.id,
            'name': tag.name,
            'color': tag.color,
            'slug': tag.slug
        } for tag in obj.tags.all()],
        'author': {
            'email': obj.author.email,
            'id': obj.author.id,
            'username': obj.author.username,
            'first_name': obj.author.first_name,
            'last_name': obj.author.last_name,
            'is_subscribed': False
        },
        "ingredients": [{
            'id': count.ingredient.id,
            'name': count.ingredient.name,
            'measurement_unit': count.ingredient.measurement_unit,
            "amount": count.amount
        } for count in obj.ingredients.all()],
        'is_favorited': False,
        'is_in_shopping_cart': False,
        'name': 'string',
        'image': obj.image.url,
        'text': obj.text,
        'cooking_time': obj.cooking_time,
    } for obj in objects]


class RecipeTestAPI(APITestCase):

    @classmethod
    @override_settings(MEDIA_ROOT=MEDIA)
    def setUpClass(cls) -> None:
        cls.user = User.objects.create(
            username='user'
        )
        cls.images = []
        for _ in range(5):
            img = Image.new('RGB', (10, 10), rnd.randint(0, 255))
            img.convert()
            with BytesIO() as b:
                img.save(b, 'jpeg')
                cls.images.append(
                    b.getvalue()
                )
        tags = TagModel.objects.bulk_create([
            TagModel(
                id=num, name=f'тэг{num}',
                slug=f'tag{num}', color=hex(num)
            ) for num in range(100)
        ])
        ingredients = IngredientModel.objects.bulk_create([
            IngredientModel(
                name=f'ингридиент {num}', id=num,
                measurement_unit=rnd.choice(('кг', 'г', 'шт')),
            ) for num in range(100)
        ])
        counts = CountModel.objects.bulk_create([
            CountModel(
                id=num, ingredient=ingredients[num],
                amount=num
            ) for num in range(100)
        ])
        recipes = RecipeModel.objects.bulk_create([
            RecipeModel(
                id=num, author=cls.user,
                # tags=[tags[num]], ingredients=[counts[num]],
                image=SimpleUploadedFile(
                    str(num), rnd.choice(cls.images),
                    content_type='jpeg'
                ),
                name=f'name {num}', cooking_time=rnd.randint(5, 50),
            ) for num in range(100)
        ])
        for tag, count, recipe in zip(tags, counts, recipes):
            recipe.tags.add(tag)
            recipe.ingredients.add(count)

    def setUp(self):
        self.guest_client = APIClient()
        self.user_client = APIClient()
        self.user_client.force_authenticate(RecipeTestAPI.user)

    @base_test
    def test_get(self):
        url = '/api/recipes/',
        data = (
            (
                {
                    # 'data': {},
                    'client': self.guest_client,
                    'method': 'get',
                },
                {
                    'http': HTTPStatus.OK,
                    **data_maping(RecipeModel.objects.all())
                }
            ),
        ),
        return url, data
        # print(requests[0][1]['data'])
        # for req, ans in requests:
        #     with self.subTest(url=req['url']):
        #         responce = req['client'].get(req['url'])
        #         self.assertEqual(responce.status_code, ans['status_code'])
        #         res_data = responce.json()
        #         self.assertEqual(res_data['results'], ans['data'])

    @check_db_test(RecipeModel, True)
    def test_post(self):
        url = '/api/recipes/'
        requests = (
            (
                {
                    'client': self.guest_client,
                    'method': 'post',
                },
                {
                    'http': status.HTTP_401_UNAUTHORIZED,
                    'detail': 'Учетные данные не были предоставлены.'
                },
            ), (
                {
                    'client': self.user_client,
                    'method': 'post',
                    'ingredients': [
                        {
                            'id': 1,
                            'amount': 10
                        }
                    ],
                    'tags': [
                        1,
                        2
                    ],
                    'image': (
                        'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAE'
                        'AAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAA'
                        'CXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCBy'
                        'xOyYQAAAABJRU5ErkJggg=='
                    ),
                    'name': 'string',
                    'text': 'string',
                    'cooking_time': 1
                },
                {
                    'http': status.HTTP_201_CREATED
                }
            )
        )
        return url, requests

    @classmethod
    def tearDownClass(cls):
        rmtree(MEDIA, ignore_errors=True)
        RecipeModel.objects.all().delete()
        TagModel.objects.all().delete()
        CountModel.objects.all().delete()
        IngredientModel.objects.all().delete()
