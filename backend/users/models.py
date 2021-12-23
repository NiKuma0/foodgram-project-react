from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.query_utils import Q
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)


class Subcribe(models.Model):
    subscriber = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='subscribed',
        verbose_name=_('subscriber')
    )
    subscribed = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name=_('subscribed')
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
        verbose_name = _('Subscribe model')
        verbose_name_plural = _('Subscribe models')

    def __str__(self) -> str:
        return f'{self.subscriber} -> {self.subscribed}'
