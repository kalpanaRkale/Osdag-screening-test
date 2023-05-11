from django.urls import include, path
from rest_framework import routers
from .views import DrawingViewSet

router = routers.DefaultRouter()
router.register(r'drawings', DrawingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
