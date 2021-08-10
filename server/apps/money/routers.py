from rest_framework import routers
from .views import CategoryViewSet, TransactionViewSet


router = routers.SimpleRouter()

router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'transactions', TransactionViewSet, basename='transaction')


urlpatterns = router.urls
