from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    UNIT_CHOICES = [
        ("each", "Each"),
        ("box", "Box"),
        ("pallet", "Pallet"),
        ("kg", "Kilogram"),
        ("liter", "Liter"),
    ]

    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, default="")
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )
    unit_of_measure = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES,
        default="each",
    )
    weight = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sku} — {self.name}"
    
class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    zone = models.CharField(max_length=50)
    aisle = models.CharField(max_length=10, blank=True, default="")
    rack = models.CharField(max_length=10, blank=True, default="")
    shelf = models.CharField(max_length=10, blank=True, default="")
    bin = models.CharField(max_length=10, blank=True, default="")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=20, unique=True)
    contact_name = models.CharField(max_length=200, blank=True, default="")
    email = models.EmailField(blank=True, default="")
    phone = models.CharField(max_length=50, blank=True, default="")
    address = models.TextField(blank=True, default="")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} — {self.name}"
