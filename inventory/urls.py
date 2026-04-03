from django.urls import path, include
from rest_framework.routers import DefaultRouter
from inventory.views import (
    CategoryViewSet,
    ProductViewSet,
    LocationViewSet,
    SupplierViewSet,
)

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"products", ProductViewSet)
router.register(r"locations", LocationViewSet)
router.register(r"suppliers", SupplierViewSet)

urlpatterns = [
    path("", include(router.urls)),
]