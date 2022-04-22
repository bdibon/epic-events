from rest_framework import routers

from .views import EmployeeModelViewSet

router = routers.SimpleRouter()
router.register(r"", EmployeeModelViewSet, basename="employee")
urlpatterns = router.urls
