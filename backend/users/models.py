from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.query_utils import Q
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(
        _('email address'), unique=True,
        help_text='Адрес электронной почты'
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)


class Subcribe(models.Model):
    subscriber = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='subscribed',
        verbose_name='подписчик',
        help_text='Подписчик'
    )
    subscribed = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='подписан',
        help_text='Подписан'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('subscriber', 'subscribed'), name='unique_link'),
            models.CheckConstraint(
                check=~Q(subscriber=models.F('subscribed')),
                name='cannot_subscribe_to_self',
            ),
        )
        verbose_name = 'Модель подписки'
        verbose_name_plural = 'Модель подписок'

    def __str__(self) -> str:
        return f'{self.subscriber} -> {self.subscribed}'
