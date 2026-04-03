from django.test import TestCase
from django.db import IntegrityError
from inventory.models import Category, Product, Location, Supplier
from rest_framework.test import APIClient
from rest_framework import status


class CategoryModelTest(TestCase):
    def test_create_category(self):
        """A category can be created with a name and description."""
        category = Category.objects.create(
            name="Electronics",
            description="Electronic devices and accessories",
        )
        self.assertEqual(category.name, "Electronics")
        self.assertEqual(str(category), "Electronics")

    def test_category_name_is_unique(self):
        """Two categories cannot have the same name."""
        Category.objects.create(name="Electronics")
        with self.assertRaises(IntegrityError):
            Category.objects.create(name="Electronics")

    def test_description_is_optional(self):
        """A category can be created without a description."""
        category = Category.objects.create(name="Furniture")
        self.assertEqual(category.description, "")


class ProductModelTest(TestCase):
    def setUp(self):
        """Create a category that all product tests can use."""
        self.category = Category.objects.create(name="Electronics")

    def test_create_product(self):
        """A product can be created with all required fields."""
        product = Product.objects.create(
            name="Wireless Mouse",
            sku="WM-001",
            category=self.category,
        )
        self.assertEqual(product.name, "Wireless Mouse")
        self.assertEqual(product.sku, "WM-001")
        self.assertEqual(product.category, self.category)
        self.assertEqual(str(product), "WM-001 — Wireless Mouse")

    def test_sku_is_unique(self):
        """Two products cannot share the same SKU."""
        Product.objects.create(
            name="Wireless Mouse",
            sku="WM-001",
            category=self.category,
        )
        with self.assertRaises(IntegrityError):
            Product.objects.create(
                name="Different Mouse",
                sku="WM-001",
                category=self.category,
            )

    def test_weight_is_optional(self):
        """A product can be created without a weight."""
        product = Product.objects.create(
            name="USB Cable",
            sku="UC-001",
            category=self.category,
        )
        self.assertIsNone(product.weight)

    def test_default_unit_of_measure(self):
        """Unit of measure defaults to 'each'."""
        product = Product.objects.create(
            name="Keyboard",
            sku="KB-001",
            category=self.category,
        )
        self.assertEqual(product.unit_of_measure, "each")

    def test_category_protect_on_delete(self):
        """Cannot delete a category that has products."""
        Product.objects.create(
            name="Monitor",
            sku="MN-001",
            category=self.category,
        )
        with self.assertRaises(Exception):
            self.category.delete()

class CategoryAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(
            name="Electronics",
            description="Electronic devices",
        )

    def test_list_categories(self):
        """GET /api/categories/ returns a list of categories."""
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Electronics")

    def test_create_category(self):
        """POST /api/categories/ creates a new category."""
        data = {"name": "Furniture", "description": "Tables and chairs"}
        response = self.client.post("/api/categories/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

    def test_retrieve_category(self):
        """GET /api/categories/<id>/ returns a single category."""
        response = self.client.get(f"/api/categories/{self.category.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Electronics")

    def test_create_category_without_name_fails(self):
        """POST /api/categories/ without a name returns 400."""
        response = self.client.post("/api/categories/", {"description": "No name"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProductAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Wireless Mouse",
            sku="WM-001",
            category=self.category,
        )

    def test_list_products(self):
        """GET /api/products/ returns a list of products."""
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_product(self):
        """POST /api/products/ creates a new product."""
        data = {
            "name": "Keyboard",
            "sku": "KB-001",
            "category": self.category.id,
        }
        response = self.client.post("/api/products/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_product_response_includes_category_name(self):
        """Product API response includes the human-readable category name."""
        response = self.client.get(f"/api/products/{self.product.id}/")
        self.assertEqual(response.data["category_name"], "Electronics")

    def test_create_product_without_sku_fails(self):
        """POST /api/products/ without a SKU returns 400."""
        data = {"name": "No SKU Product", "category": self.category.id}
        response = self.client.post("/api/products/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_duplicate_sku_fails(self):
        """POST /api/products/ with a duplicate SKU returns 400."""
        data = {
            "name": "Another Mouse",
            "sku": "WM-001",
            "category": self.category.id,
        }
        response = self.client.post("/api/products/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class LocationModelTest(TestCase):
    def test_create_location(self):
        """A location can be created with all fields."""
        location = Location.objects.create(
            name="A-03-02-04",
            zone="A",
            aisle="03",
            rack="02",
            shelf="04",
        )
        self.assertEqual(location.name, "A-03-02-04")
        self.assertEqual(str(location), "A-03-02-04")
        self.assertTrue(location.is_active)

    def test_location_name_is_unique(self):
        """Two locations cannot have the same name."""
        Location.objects.create(name="A-01-01-01", zone="A")
        with self.assertRaises(IntegrityError):
            Location.objects.create(name="A-01-01-01", zone="A")

    def test_location_with_zone_only(self):
        """A location can be created with just a name and zone."""
        location = Location.objects.create(
            name="Receiving Dock",
            zone="Receiving",
        )
        self.assertEqual(location.aisle, "")
        self.assertEqual(location.rack, "")


class SupplierModelTest(TestCase):
    def test_create_supplier(self):
        """A supplier can be created with all fields."""
        supplier = Supplier.objects.create(
            name="Acme Corp",
            code="SUP-001",
            contact_name="John Smith",
            email="john@acme.com",
            phone="+1-555-0100",
        )
        self.assertEqual(supplier.name, "Acme Corp")
        self.assertEqual(str(supplier), "SUP-001 — Acme Corp")
        self.assertTrue(supplier.is_active)

    def test_supplier_code_is_unique(self):
        """Two suppliers cannot share the same code."""
        Supplier.objects.create(name="Acme Corp", code="SUP-001")
        with self.assertRaises(IntegrityError):
            Supplier.objects.create(name="Other Corp", code="SUP-001")

    def test_contact_fields_are_optional(self):
        """A supplier can be created with just name and code."""
        supplier = Supplier.objects.create(name="MinimalCo", code="SUP-002")
        self.assertEqual(supplier.contact_name, "")
        self.assertEqual(supplier.email, "")
        self.assertEqual(supplier.phone, "")


class LocationAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.location = Location.objects.create(
            name="A-01-01-01",
            zone="A",
            aisle="01",
            rack="01",
            shelf="01",
        )

    def test_list_locations(self):
        """GET /api/locations/ returns a list of locations."""
        response = self.client.get("/api/locations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_location(self):
        """POST /api/locations/ creates a new location."""
        data = {"name": "B-02-01-01", "zone": "B", "aisle": "02"}
        response = self.client.post("/api/locations/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 2)

    def test_create_location_without_zone_fails(self):
        """POST /api/locations/ without a zone returns 400."""
        data = {"name": "No Zone"}
        response = self.client.post("/api/locations/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicate_name_fails(self):
        """POST /api/locations/ with a duplicate name returns 400."""
        data = {"name": "A-01-01-01", "zone": "A"}
        response = self.client.post("/api/locations/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SupplierAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.supplier = Supplier.objects.create(
            name="Acme Corp",
            code="SUP-001",
            email="info@acme.com",
        )

    def test_list_suppliers(self):
        """GET /api/suppliers/ returns a list of suppliers."""
        response = self.client.get("/api/suppliers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_supplier(self):
        """POST /api/suppliers/ creates a new supplier."""
        data = {"name": "Global Parts", "code": "SUP-002"}
        response = self.client.post("/api/suppliers/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Supplier.objects.count(), 2)

    def test_create_supplier_without_code_fails(self):
        """POST /api/suppliers/ without a code returns 400."""
        data = {"name": "No Code Inc"}
        response = self.client.post("/api/suppliers/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicate_code_fails(self):
        """POST /api/suppliers/ with a duplicate code returns 400."""
        data = {"name": "Other Corp", "code": "SUP-001"}
        response = self.client.post("/api/suppliers/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_supplier(self):
        """GET /api/suppliers/<id>/ returns a single supplier."""
        response = self.client.get(f"/api/suppliers/{self.supplier.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Acme Corp")
        self.assertEqual(response.data["email"], "info@acme.com")
