from rest_framework import status
from rest_framework.test import APIClient, APITestCase


def base_test(test, with_yield=False):
    '''Decorator for test func'''
    def wrapper(self: APITestCase,):
        url, requests_answers = test(self)
        for idx, (request, answer) in enumerate(requests_answers):
            client: APIClient = request.pop('client')
            method = request.pop('method', 'get')
            code = answer.pop('http', None)
            with self.subTest(url=url):
                responce = getattr(client, method)(url, data=request)
                self.assertEqual(
                    responce.status_code, code, msg=f'in {idx} fixture'
                )
                self.assertEqual(
                    responce.json(), answer, msg=f'in {idx} fixture'
                ) if answer else None
            if with_yield:
                yield code
    return wrapper


def check_db_test(model, only_with_pass_val=False):
    def decor(test):
        base_wrapper = base_test(test)
        if only_with_pass_val:
            base_wrapper = only_with_pass_val_test(test, True)

        def wrapper(self: APITestCase):
            count = model.objects.all().count()
            for code in base_wrapper(self):
                new_count = model.objects.all().count()
                if code == status.HTTP_201_CREATED:
                    self.assertLessEqual(
                        count, new_count,
                        f'Object "{model.__name__}" not created.'
                    )
                elif code == status.HTTP_204_NO_CONTENT:
                    self.assertGreaterEqual(
                        count, new_count,
                        f'Object "{model.__name__}" not deleted.'
                    )
                else:
                    self.assertEqual(
                        count, new_count,
                        f'The object "{model.__name__}" '
                        'was created or deleted"'
                    )
                count = new_count
        return wrapper
    return decor


def only_with_pass_val_test(test, with_yield=False):
    def wrapper(self: APITestCase,):
        url, requests_answers = test(self)
        for idx, (request, answer) in enumerate(requests_answers):
            client: APIClient = request.pop('client')
            method = request.pop('method', 'get')
            code = answer.pop('http', None)
            with self.subTest(url=url):
                responce = getattr(client, method)(url, data=request)
                self.assertEqual(
                    responce.status_code, code,
                    f'in {idx} fixture, {responce.json()}'
                )
                res_data = responce.json()
                for name, value in answer.items():
                    res_val = res_data[name]
                    self.assertEqual(
                        res_val, value,
                        f'{str({name: res_val})} != {str({name: value})}'
                        f'; in {idx} fixture'
                    )
            if with_yield:
                yield code
    return wrapper


class CallInEq:
    '''
    Calling a func with params into __eq__
    '''
    def __init__(self, func, attr=None, **params) -> None:
        self.func, self.params = func, params
        self.attr = attr
        self.__str = 'not called'

    @property
    def value(self):
        instance = self.func(**self.params)
        if self.attr:
            return getattr(instance, self.attr)
        return instance

    def __eq__(self, o: object) -> bool:
        instance = self.value
        return instance == o

    def __repr__(self) -> str:
        return str(self.value)


class Num:
    def __eq__(self, o: object) -> bool:
        return bool(isinstance(o, int) or int(o))


class Text:
    def __eq__(self, o: object) -> bool:
        return isinstance(o, str)
