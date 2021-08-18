from rest_framework import routers
from .viewsets import CategoryViewSet, TransactionViewSet, WidgetViewSet


router = routers.SimpleRouter()

router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'widgets', WidgetViewSet, basename='widget')


urlpatterns = router.urls
