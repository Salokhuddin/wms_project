from django.urls import path, include
from rest_framework.routers import DefaultRouter
from inventory.views import (
    CategoryViewSet,
    ProductViewSet,
    LocationViewSet,
    SupplierViewSet,
    InventoryViewSet,
)

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"products", ProductViewSet)
router.register(r"locations", LocationViewSet)
router.register(r"suppliers", SupplierViewSet)
router.register(r"inventory", InventoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
