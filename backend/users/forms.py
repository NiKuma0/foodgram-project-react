from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from users.models import Subcribe


class SubscribeForm(ModelForm):
    class Meta:
        model = Subcribe
        fields = ('subscriber', 'subscribed')

    def clean(self):
        cleaned_data = super().clean()
        subscriber = cleaned_data.get('subscriber', 1)
        subscribed = cleaned_data.get('subscribed', 0)
        if subscribed == subscriber:
            raise ValidationError(
                _('You cannot subscribe to yourself')
            )
        return cleaned_data
