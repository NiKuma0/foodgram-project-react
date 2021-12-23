from django.contrib.auth import get_user_model, base_user
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from tools.tests import base_test, CallInEq, check_db_test

User: base_user.AbstractBaseUser = get_user_model()


class UserTestAPI(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create(
            email='user@example.com',
            username='string',
            first_name='Вася',
            last_name='Пупкин',
        )
        cls.admin = User.objects.create(
            email='admin@fake.com', username='admin', is_staff=True,
            is_superuser=True
        )

    def setUp(self) -> None:
        self.guest_client = APIClient()
        self.user_client = APIClient()
        self.admin_client = APIClient()
        self.user_client.force_authenticate(UserTestAPI.user)
        self.admin_client.force_authenticate(UserTestAPI.admin)

    @check_db_test(User)
    def test_create(self):
        url = '/api/users/'
        requests_answers = (
            {
                'client': self.guest_client,
                'method': 'post',
                'email': 'vpupkin@yandex.ru',
                'username': 'vasya.pupkin',
                'first_name': 'Вася',
                'last_name': 'Пупкин',
                'password': 'Qwerty123'
            },
            {
                'email': 'vpupkin@yandex.ru',
                'username': 'vasya.pupkin',
                'first_name': 'Вася',
                'last_name': 'Пупкин',
                'id': CallInEq(
                    User.objects.get, 'id', email='vpupkin@yandex.ru'),
                'http': status.HTTP_201_CREATED
            }
        ), (
            {
                'client': self.guest_client,
                'method': 'post'
            },
            {
                'username': ['Обязательное поле.'],
                'first_name': ['Обязательное поле.'],
                'last_name': ['Обязательное поле.'],
                'password': ['Обязательное поле.'],
                'email': ['Обязательное поле.'],
                'http': status.HTTP_400_BAD_REQUEST,
            }
        ),
        return url, requests_answers

    @base_test
    def test_me(self):
        url = '/api/users/me/'
        request_answer = (
            {
                'method': 'get',
                'client': self.guest_client,
            },
            {
                'detail': 'Учетные данные не были предоставлены.',
                'http': status.HTTP_401_UNAUTHORIZED
            }
        ), (
            {
                'method': 'get',
                'client': self.user_client,
            },
            {
                'email': 'user@example.com',
                'id': CallInEq(
                    User.objects.get, 'id', username='string'
                ),
                'username': 'string',
                'first_name': 'Вася',
                'last_name': 'Пупкин',
                'is_subscribed': False,
                'http': status.HTTP_200_OK,
            }
        )
        return url, request_answer

    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()
