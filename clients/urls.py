from rest_framework import routers

from .views import ClientModelViewSet

router = routers.SimpleRouter()
router.register(r"", ClientModelViewSet, basename="client")

urlpatterns = router.urls
