from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.forms import SubscribeForm
from users.models import SubcribeModel, User


@admin.register(SubcribeModel)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'subscribed', 'id')
    search_field = ('subscriber', 'subscribed', 'id')
    form = SubscribeForm


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('email', 'id')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
