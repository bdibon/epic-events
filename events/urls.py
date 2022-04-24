from rest_framework import routers

from .views import ContractsViewSet, EventsViewSet

router = routers.SimpleRouter()
router.register("events", EventsViewSet)
router.register("contracts", ContractsViewSet)

urlpatterns = router.urls
