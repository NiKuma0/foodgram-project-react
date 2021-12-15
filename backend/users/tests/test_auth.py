from django.contrib.auth import get_user_model, base_user
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from tools.tests import CallInEq, base_test

User: base_user.AbstractBaseUser = get_user_model()


class TestAuthCase(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user: User = User.objects.create(
            username='admin', email='admin@fake.com',
        )
        cls.user.set_password('admin')
        cls.user.save()

    def setUp(self) -> None:
        self.client = APIClient()

    @base_test
    def test_1(self):
        url = '/api/auth/token/login/'
        data = ({
            'method': 'post',
            'client': self.client,
            'password': 'admin',
            'email': 'admin@fake.com',
        }, {
            'auth_token': CallInEq(
                Token.objects.get, 'key', user=TestAuthCase.user
            ),
            'http': status.HTTP_200_OK
        }),
        return url, data

    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()
