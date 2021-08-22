from django.urls import path, include
from .yasg import urlpatterns_doc


urlpatterns = [
    path('users/', include('apps.users.urls')),
    path('money/', include('apps.money.routers')),
]

urlpatterns += urlpatterns_doc
