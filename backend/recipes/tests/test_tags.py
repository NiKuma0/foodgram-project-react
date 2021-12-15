import random as rnd

from http import HTTPStatus
from rest_framework.test import APIClient, APITestCase

from recipes.models import TagModel


class TagTestAPI(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.tags = [
            TagModel(
                id=num, name=f'тэг{num}',
                slug=f'tag{num}', color=hex(num)
            ) for num in range(100)
        ]
        TagModel.objects.bulk_create(cls.tags)

    def setUp(self) -> None:
        self.client = APIClient()

    def test_get_tags(self):
        url = '/api/tags/'
        tags = TagModel.objects.all()
        answer = [
            {
                'id': tag.id, 'name': tag.name,
                'slug': tag.slug, 'color': tag.color
            } for tag in tags
        ]
        with self.subTest(url=url):
            responce = self.client.get(url)
            self.assertEqual(responce.status_code, HTTPStatus.OK)
            self.assertEqual(responce.json(), answer)

    def test_get_tag(self):
        id = rnd.randint(0, 99)
        url = f'/api/tags/{id}/'
        tag = TagModel.objects.get(id=id)
        answer = {
            'id': tag.id, 'name': tag.name,
            'slug': tag.slug, 'color': tag.color
        }
        with self.subTest(url=url):
            responce = self.client.get(url)
            self.assertEqual(responce.status_code, HTTPStatus.OK)
            self.assertEqual(responce.json(), answer)

    @classmethod
    def tearDownClass(cls):
        TagModel.objects.all().delete()
