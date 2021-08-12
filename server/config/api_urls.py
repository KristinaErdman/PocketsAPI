from django.urls import path, include

urlpatterns = [
    path('users/', include('apps.users.urls')),
    path('money/', include('apps.money.routers')),
]
