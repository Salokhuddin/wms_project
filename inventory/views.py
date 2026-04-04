from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from inventory.models import Category, Product, Location, Supplier, Inventory
from inventory.serializers import (
    CategorySerializer, 
    ProductSerializer, 
    LocationSerializer, 
    SupplierSerializer,
    InventorySerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    @action(detail=False, methods=["get"], url_path="by-product/(?P<product_id>[^/.]+)")
    def by_product(self, request, product_id=None):
        """Where is product X? Returns all locations holding this product."""
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        records = Inventory.objects.filter(product=product, quantity__gt=0)
        serializer = self.get_serializer(records, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="by-location/(?P<location_id>[^/.]+)")
    def by_location(self, request, location_id=None):
        """What's in location Y? Returns all products at this location."""
        try:
            location = Location.objects.get(id=location_id)
        except Location.DoesNotExist:
            return Response(
                {"error": "Location not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        records = Inventory.objects.filter(location=location, quantity__gt=0)
        serializer = self.get_serializer(records, many=True)
        return Response(serializer.data)
