from django.db import models
from home_and_auth.models import *

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='categoyr_images/',null=True)
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='subcatgeory_images/',null=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    quantity = models.IntegerField(default=0)
    event = models.ForeignKey(SliderItem, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    material = models.CharField(max_length=100, null=True)  # New field for material
    weight = models.DecimalField(max_digits=10,null=True, decimal_places=2)  # New field for weight
    warranty_policy = models.TextField(null=True)  # New field for warranty policy
    warranty_year = models.IntegerField(null=True)  # New field for warranty year

    def __str__(self):
        return self.name

class Inventory(models.Model):
    IN_STOCK = 'In stock'
    STOCK_OUT = 'Stock out'
    AVAILABILITY_CHOICES = [
        (IN_STOCK, 'In stock'),
        (STOCK_OUT, 'Stock out'),
    ]
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='inventory')
    quantity_available = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default=IN_STOCK)

    def __str__(self):
        return f"{self.product.name} Inventory"

class Color(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='colors')

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/',null=True)

    def __str__(self):
        return f"Image for {self.product.name}"