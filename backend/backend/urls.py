from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/', include('users.urls')),
    path('api/', include('recipes.urls')),
]
