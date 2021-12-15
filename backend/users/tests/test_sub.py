from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from tools.tests import base_test, check_db_test, Text
from users.models import SubcribeModel

User = get_user_model()


class TestSubAPI(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user1 = User.objects.create(
            email='user1@email.com',
            username='user1',
            id=1
        )
        cls.user2 = User.objects.create(
            email='user2@mail.com',
            username='user2',
            id=2
        )
        cls.user3 = User.objects.create(
            email='user3@mail.com',
            username='user3',
            id=3
        )

    def setUp(self) -> None:
        self.client1 = APIClient()
        self.client2 = APIClient()
        self.client3 = APIClient()
        self.client1.force_authenticate(TestSubAPI.user1)
        self.client2.force_authenticate(TestSubAPI.user2)
        self.client3.force_authenticate(TestSubAPI.user3)

    @check_db_test(SubcribeModel)
    def test_sub(self):
        url = '/api/users/2/subscribe/'
        data = (
            {
                'client': self.client1,
                'method': 'get'
            },
            {
                'http': status.HTTP_201_CREATED,
            }
        ), (
            {
                'client': self.client1,
                'method': 'get',
            },
            {
                'http': status.HTTP_400_BAD_REQUEST,
                'errors': ['You have already subscribed']
            }
        ), (
            {
                'client': self.client1,
                'method': 'delete',
            },
            {
                'http': status.HTTP_204_NO_CONTENT
            }
        )
        return url, data

    @base_test
    def test_get_subs(self):
        SubcribeModel.objects.create(
            subscriber=TestSubAPI.user1,
            subscribed=TestSubAPI.user2
        )
        url = '/api/users/subscriptions/'
        data = (
            {
                'client': self.client1,
                'method': 'get',
            },
            {
                'http': status.HTTP_200_OK,
            }
        ), (
            {
                'client': self.client2,
                'method': 'get'
            },
            {
                'http': status.HTTP_200_OK,
                'count': 0,
                'next': Text(),
                'previous': Text(),
                'result': []
            }
        )
        return url, data

    def tearDown(self) -> None:
        SubcribeModel.objects.all().delete()
